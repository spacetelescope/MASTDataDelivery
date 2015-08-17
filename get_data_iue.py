"""
.. module:: get_data_iue

   :synopsis: Returns IUE spectral data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

from astropy.io import fits
import collections
from data_series import DataSeries
import numpy
from operator import itemgetter
from parse_obsid_iue import parse_obsid_iue

#--------------------
def order_combine(order_spectra, camera):
    """
    Combine spectral orders following Solano's definition of how to cut each
    order's spectrum to deal with overlap.

    :param order_spectra: A list containing the wavelengths, fluxes, and order
    numbers for each spectral order, stored as dicts.

    :type order_spectra: list

    :param camera: The camera used for this spectrum, either "SWP", "LWR", or
    "LWP".

    :type camera: str

    :returns: list -- combined wavelength, flux pairs
    """
    all_wls = []
    all_fls = []
    for ord_ind in xrange(len(order_spectra)-1):
        # Current order ("m").
        wls1 = order_spectra[ord_ind]['wls']
        fls1 = order_spectra[ord_ind]['fls']

        # Next order ("m-1").
        wls2 = order_spectra[ord_ind+1]['wls']
        fls2 = order_spectra[ord_ind+1]['fls']

        # Determin the cut wavelength following Equation 1 and 2 from Solano.
        if camera in ["LWP", "LWR"]:
            cut_wl = wls2[0] + 2. * (wls1[-1]-wls2[0])/3.
        else:
            cut_wl = wls2[0] + (wls1[-1]-wls2[0])/3.

        # Keep those wavelengths from the two orders that don't cross the cut.
        keep1 = numpy.where(numpy.asarray(wls1) <= cut_wl)[0]
        keep2 = numpy.where(numpy.asarray(wls2) > cut_wl)[0]
        order_spectra[ord_ind]['wls'] = [wls1[i] for i in keep1]
        order_spectra[ord_ind]['fls'] = [fls1[i] for i in keep1]
        order_spectra[ord_ind+1]['wls'] = [wls2[i] for i in keep2]
        order_spectra[ord_ind+1]['fls'] = [fls2[i] for i in keep2]

    # Concatenate the trimmed order spectra.
    for ord_ind in xrange(len(order_spectra)):
        all_wls.extend(order_spectra[ord_ind]['wls'])
        all_fls.extend(order_spectra[ord_ind]['fls'])
    return zip(all_wls, all_fls)
#--------------------

#--------------------
def calculate_cut_wl(camera, order, aperture):
    """
    Calculate the cut wavelength for an order following Solano's paper.

    :param camera: The camera used.

    :type camera: str

    :param order: The order number.

    :type order: float

    :param aperture: The aperture used.

    :type aperture: str

    :returns: float -- The cut wavelength for this order.
    """
    # NOTE: When I tried to use it I did not get cut wavelengths that fell
    # within the order's range, either the equation is wrong or I am applying it
    # wrong.
    if camera == "LWP":
        if order >= 77 and order <= 124:
            if aperture == "LARGE":
                cut_wl = -7.9697 + 233257.6280/order
            else:
                cut_wl = -7.7959 + 233382.6450/order
        else:
            # Non-overlap orders, just return a very large wavelength.
            cut_wl = 9E9
    elif camera == "LWR":
        if order >= 76 and order <= 119:
            if aperture == "LARGE":
                cut_wl = -11.3459 + 233737.5903/order
            else:
                cut_wl = -11.2214 + 233876.9950/order
        else:
            cut_wl = 9E9
    else:
        # The only other camera option is SWP.
        if order >= 73 and order <= 120:
            if aperture == "LARGE":
                cut_wl = 24.3952 + 132875.4838/order + 325840.9715/(order*order)
            else:
                cut_wl = 22.2095 + 133293.4862/order + 300351.2209/(order*order)
        else:
            cut_wl = 9E9
    return cut_wl
#--------------------

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
                        # Get the aperture from the primary header.
                        aperture = hdulist[0].header["aperture"].strip()
                        # Get the dispersion type from the primary header.
                        dispersion = hdulist[0].header["disptype"].strip()
                        # Get the camera used (SWP, LWP, LWR).
                        camera = hdulist[0].header["camera"].strip()
                        # Get a list of spectral orders.  Those that are beyond
                        # the range defined in Solano are not considered.
                        if camera == "LWP":
                            max_order = 124
                        elif camera == "LWR":
                            max_order = 119
                        else:
                            max_order = 120
                        orders = [int(x) for x in hdulist[1].data["order"] if x
                                  <= max_order]
                        n_orders = len(orders)
                        # This lists will store each orders' spectral info.
                        order_spectra = []

                        # Loop over each order.
                        for order in range(n_orders):
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
                            # Extract the quality flags that go along with
                            # these wls.
                            all_qfs = hdulist[1].data["quality"][order]
                            qfs = [int(x) for x in all_qfs[(s_pix-1):(s_pix-1+
                                                                      n_p-1+1)]]
                            # Only keep good Quality Flags, if the order is all
                            # bad flags, don't add it.
                            keep = [i for i, x in enumerate(qfs) if (qfs[i] >
                                                                     -16384)]
                            if keep != [] and fls != [0.]*len(fls):
                                wls = [wls[i] for i in keep]
                                fls = [fls[i] for i in keep]
                                # Create a dict that will store this order's
                                # info.
                                order_spec = {'order':orders[order], 'wls':wls,
                                              'fls':fls}
                                order_spectra.append(order_spec)

                        # Order-combine the spectra.
                        comb_spec = order_combine(order_spectra, camera)

                        # Create the return structures.
                        all_plot_xunits.append(iue_xunit)
                        all_plot_yunits.append(iue_yunit)
                        all_plot_series.append([data_point(x=x, y=y) for
                                                x, y in comb_spec])
                        all_plot_labels.append('IUE_' + obsid + ' DISP:' +
                                               dispersion + ' APER:' + aperture)
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
