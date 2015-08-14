"""
.. module:: get_data_iue

   :synopsis: Returns IUE spectral data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

from astropy.io import fits
import collections
from data_series import DataSeries
from operator import itemgetter
from parse_obsid_iue import parse_obsid_iue

#--------------------
def get_data_iue(obsid):
    """
    Given an IUE observation ID, returns the spectral data.  Note that, in some
    cases, an observation ID has both a low and high dispersion spectrum
    available.  In that event, both the low and high dispersion spectra are
    returned as data series, regardless of whether the user wanted one or both.

    :param obsid: The IUE observation ID to retrieve the data from.

    :type obsid: str

    :returns: JSON -- The spectral data for this observation ID.

    Error codes:
    From parse_obsid_iue:
    0 = No error parsing observation ID.
    1 = Observation ID does not begin with expected first three letters.
    2 = No mxlo or mxhi file found on disk.
    From this module:
    3 = Could not open one or more FITS file for reading.
    """

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For IUE, this defines the x-axis and y-axis units as a string.
    iue_xunit = "Angstroms (vacuum, heliocentric)"
    iue_yunit = "ergs/cm^2/s/Angstrom"

    # Parse the obsID string to determine the paths+files to read.  Note:
    # this step will assign some of the error codes returned to the top level.
    parsed_files_result = parse_obsid_iue(obsid)

    # These lists will store the spectral information for each data series.
    all_plot_xunits = []
    all_plot_yunits = []
    all_plot_labels = []
    all_plot_series = []

    # For each file, read in the contents and create a return JSON object.
    if parsed_files_result.errcode == 0:
        for sfile in parsed_files_result.specfiles:
            # Figure out if this is an mxhi or mxlo spectrum.
            if sfile[-7:] == "mxlo.gz":
                is_lo = True
                is_hi = False
            else:
                is_lo = False
                is_hi = True

            # This error code will be used unless there's a problem reading any
            # of the FITS files in the list.
            errcode = 0

            try:
                with fits.open(sfile) as hdulist:
                    if is_lo:
                        # Get the dispersion type from the primary header.
                        dispersion = hdulist[0].header["disptype"]
                        # Get the aperture size(s) from the header.
                        apertures = hdulist[1].data["aperture"]
                        n_apertures = len(apertures)
                        # Number of spectral data points for each aperture size.
                        n_wls = [int(x) for x in hdulist[1].data["npoints"]]
                        # Initial wavelength value(s).
                        starting_wl = [float(x) for x in
                                       hdulist[1].data["wavelength"]]
                        # Step size(s) for each subsequent wavelength.
                        delta_wl = [float(x) for x in hdulist[1].data["deltaw"]]
                        # Generate the full array of wavelength values, and get
                        # full array of flux values, for each  aperture.
                        for aper in xrange(n_apertures):
                            wls = [starting_wl[aper] +
                                   x*delta_wl[aper] for
                                   x in xrange(n_wls[aper])]
                            fls = [float(x) for
                                   x in hdulist[1].data["flux"][aper]]
                            # Make sure wavelengths and fluxes are sorted
                            # from smallest wavelength to largest.
                            sort_indexes = [x[0] for x in
                                            sorted(enumerate(wls),
                                                   key=itemgetter(1))]
                            wls = [wls[x] for x in sort_indexes]
                            fls = [fls[x] for x in sort_indexes]
                            wlfls = [(x, y) for x, y in zip(wls, fls) if
                                     y != 0.]
                            if wlfls != []:
                                all_plot_xunits.append(iue_xunit)
                                all_plot_yunits.append(iue_yunit)
                                all_plot_series.append([data_point(x=x, y=y) for
                                                        x, y in wlfls])
                                all_plot_labels.append(('IUE_' + obsid +
                                                        ' DISP:' + dispersion +
                                                        ' APER:' +
                                                        apertures[aper]))
                    if is_hi:
                        # Get a list of spectral orders.
                        orders = [int(x) for x in hdulist[1].data["order"]]
                        n_orders = len(orders)
                        # Get the aperture from the primary header.
                        aperture = hdulist[0].header["aperture"].strip()
                        # Get the dispersion type from the primary header.
                        dispersion = hdulist[0].header["disptype"].strip()
                        # These lists will store all the orders' wls and fls.
                        spec_wls = []
                        spec_fls = []
                        # Loop over each order.
                        for order in xrange(n_orders):
                            # Number of fluxes for this order.
                            n_p = int(hdulist[1].data["npoints"][order])
                            # Starting pixel within the array of 768 elements.
                            s_pix = int(
                                hdulist[1].data["startpix"][order])
                            # Wavelength corresponding to this start pixel.
                            starting_wl = float(
                                hdulist[1].data["wavelength"][order])
                            # Step size for each subsequent wavelength.
                            delta_wl = float(
                                hdulist[1].data["deltaw"][order])
                            # Generate the full array of wavelength values.
                            wls = [starting_wl + x*delta_wl for x in
                                   xrange(n_p)]
                            # Extract the fluxes that go along with these wls.
                            all_fluxes = hdulist[1].data["abs_cal"][order]
                            fls = [float(x) for x in
                                   all_fluxes[(s_pix-1):(s_pix-1+n_p-1+1)]]
                            # Add the wls and fls to the master lists.
                            spec_wls.extend(wls)
                            spec_fls.extend(fls)

                        # Make sure wavelengths and fluxes are sorted
                        # from smallest wavelength to largest.
                        sort_indexes = [x[0] for x in
                                        sorted(enumerate(spec_wls),
                                               key=itemgetter(1))]
                        spec_wls = [spec_wls[x] for x in sort_indexes]
                        spec_fls = [spec_fls[x] for x in sort_indexes]
                        wlfls = [(x, y) for x, y in zip(spec_wls, spec_fls) if
                                 y != 0.]
                        if wlfls != []:
                            all_plot_xunits.append(iue_xunit)
                            all_plot_yunits.append(iue_yunit)
                            all_plot_series.append([data_point(x=x, y=y) for
                                                    x, y in wlfls])
                            all_plot_labels.append(
                                'IUE_' + obsid +
                                ' DISP:' + dispersion +
                                ' APER:' + aperture)
            except IOError:
                errcode = 3
                all_plot_labels.append('')
                all_plot_series.append([])
                all_plot_xunits.append('')
                all_plot_yunits.append('')

        # Create the return DataSeries object.
        return_dataseries = DataSeries('iue', obsid, all_plot_series,
                                       all_plot_labels,
                                       all_plot_xunits, all_plot_yunits,
                                       errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries('iue', obsid, [], [], [], [],
                                       parsed_files_result.errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
