"""
.. module:: get_data_iue

   :synopsis: Returns IUE spectral data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

from astropy.io import fits
import collections
from data_series import DataSeries
import math
import numpy
from operator import itemgetter
from parse_obsid_iue import parse_obsid_iue
from scipy.interpolate import interp1d

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
def interpolate_subspec(wls, fls, prev_index, gap_ind, wl_step):
    """
    Interpolates a subsection of a spectrum (from prev_index to gap_index) onto
    a new grid.

    :param wls: List of subsection wavelengths.

    :type wls: list

    :param fls: List of subsection fluxes.

    :type fls: list

    :param prev_index: Starting index of subsection.

    :type prev_index: int

    :param gap_ind: Ending index of subsection.

    :type gap_ind: int

    :param wl_step: Wavelength step size to use for interpolated spectrum.

    :type wl_step: float

    :returns: tuple -- (list of int. wavelengths, list of int. fluxes)
    """
    # Get the subspectrum
    sub_spec_wls = wls[prev_index:gap_ind+1]
    sub_spec_fls = fls[prev_index:gap_ind+1]
    # Interpolate onto the new grid, using linear interpolation.
    interp_f = interp1d(sub_spec_wls, sub_spec_fls, kind="linear")

    # Calculate the number of linear wavelength steps needed.
    min_wl = min(sub_spec_wls)
    max_wl = max(sub_spec_wls)
    n_steps = math.ceil((max_wl - min_wl) / wl_step)
    # Try a couple step sizes to get as close to the ideal size as possible.
    new_wls1, step_size1 = numpy.linspace(min_wl, max_wl, n_steps,
                                          retstep=True)
    new_wls2, step_size2 = numpy.linspace(min_wl, max_wl, n_steps+1,
                                          retstep=True)
    new_wls3, step_size3 = numpy.linspace(min_wl, max_wl, n_steps-1,
                                          retstep=True)
    # Choose the linear step size closest to our desired step size.
    diffs = [abs(x-wl_step) for x in [step_size1, step_size2, step_size3]]
    if diffs[0] <= diffs[1] and diffs[0] <= diffs[2]:
        new_wls = new_wls1
    elif diffs[1] <= diffs[2] and diffs[1] <= diffs[0]:
        new_wls = new_wls2
    else:
        new_wls = new_wls3
    # Calculate the interpolated values and extend the spectrum with them.
    return (list(new_wls), list(interp_f(new_wls)))
#--------------------

#--------------------
def order_combine(order_spectra, camera, showplot=False):
    """
    Combine spectral orders following Solano's definition of how to cut each
    order's spectrum to deal with overlap.

    :param order_spectra: A list containing the wavelengths, fluxes, and order
    numbers for each spectral order, stored as dicts.  The wavelengths and
    fluxes are numpy.ndarrays

    :type order_spectra: list

    :param camera: The camera used for this spectrum, either "SWP", "LWR", or
    "LWP".

    :type camera: str

    :param showplot: Set to true to show a plot of the original vs. interpolated
    spectrum (default = False, only set when debugging).

    :type showplot: bool

    :returns: list -- combined wavelength, flux pairs
    """
    # These lists will hold the order-combined wavelengths and spectra.
    all_wls = []
    all_fls = []

    for ord_ind in xrange(len(order_spectra)-1):
        # Current order ("m").
        wls1 = order_spectra[ord_ind]['wls']
        fls1 = order_spectra[ord_ind]['fls']

        # Next order ("m-1").
        wls2 = order_spectra[ord_ind+1]['wls']
        fls2 = order_spectra[ord_ind+1]['fls']

        # Determine the cut wavelength following Equations 1 and 2 from Solano.
        if camera in ["LWP", "LWR"]:
            cut_wl = wls2[0] + 2. * (wls1[-1]-wls2[0])/3.
        else:
            cut_wl = wls2[0] + (wls1[-1]-wls2[0])/3.

        if showplot:
            import matplotlib.pyplot as pyp
            pyp.plot(wls1, fls1, 'bo')
            pyp.plot(wls2, fls2, 'ro')
            pyp.axvline(cut_wl)
            pyp.show()

        # Keep those wavelengths from the two orders that don't cross the cut.
        keep1 = numpy.where(wls1 <= cut_wl)[0]
        keep2 = numpy.where(wls2 > cut_wl)[0]
        order_spectra[ord_ind]['wls'] = wls1[keep1]
        order_spectra[ord_ind]['fls'] = fls1[keep1]
        order_spectra[ord_ind+1]['wls'] = wls2[keep2]
        order_spectra[ord_ind+1]['fls'] = fls2[keep2]
        # Update the order that has already been trimmed on both sides.
        all_wls.extend(order_spectra[ord_ind]['wls'])
        all_fls.extend(order_spectra[ord_ind]['fls'])
        # If this is the second-to-last order, update the last order as well,
        # since that is only trimmed on one side.
        if ord_ind == len(order_spectra)-2:
            all_wls.extend(order_spectra[ord_ind+1]['wls'])
            all_fls.extend(order_spectra[ord_ind+1]['fls'])

    return zip(all_wls, all_fls)
#--------------------

#--------------------
def resample_spectrum(combined_spectrum, camera, showplot=False):
    """
    Resamples the order-combined spectrum to an evenly-sampled wavelength scale.

    :param combined_spectrum: The order-combined spectrum with unequal
    wavelength sampling.  It is a list of (wl,fl) tuples.

    :type combined_spectrum: list

    :param camera: The camera used for this spectrum, either "SWP", "LWR", or
    "LWP".

    :type camera: str

    :param showplot: Set to true to show a plot of the original vs. interpolated
    spectrum (default = False, only set when debugging).

    :type showplot: bool

    :returns: list -- A list of (wl,fl) tuples of the evenly-sampled spectrum.
    """

    # Unpack the wavelengths and fluxes.
    wls, fls = zip(*combined_spectrum)

    # Generate the re-sampled x-axis, starting at the min. wavelength and ending
    # at the max. wavelength.  The final bin size should be 0.05 Ang. for SWP
    # cameras or 0.10 Ang. for LWP and LWR cameras.  We oversample by a factor
    # of 10 before binning down.
    oversample = 10.
    if camera in ["LWP", "LWR"]:
        wl_step = 0.1 / oversample
    else:
        wl_step = 0.05 / oversample

    # Identify gaps in the data, interpolate those gaps separately so you don't
    # interpolate over a gap.  A gap is defined as anywhere with more than three
    # missing points (based on the mean wavelength difference across the
    # spectrum).
    wl_diffs = numpy.diff(wls)
    # These are the *end points* of a given subsection.
    wl_gaps = numpy.where(numpy.digitize(wl_diffs, [3.*numpy.mean(wl_diffs)]) !=
                          0)[0]
    # If there are no gaps at all, then define the gap to be the last element.
    if len(wl_gaps) == 0:
        wl_gaps = numpy.asarray([len(wls)-1])

    # Build the binned spectrum for each subspectrum (skipping over gaps).
    prev_index = 0
    binned_wls = []
    binned_fls = []
    # Only build up the interpolated spectrum if it is to be plotted.
    if showplot:
        interpolated_wls = []
        interpolated_fls = []

    for gap_ind in wl_gaps:
        # Get interpolated spectrum for this subsection.
        new_wls, new_fls = interpolate_subspec(wls, fls, prev_index, gap_ind,
                                               wl_step)
        # Push the interpolated values into the list via extension, but only if
        # it is to be plotted.
        if showplot:
            interpolated_wls.extend(new_wls)
            interpolated_fls.extend(new_fls)
        # Now bin the spectrum down by a factor of 10 in resolution to our
        # desired wavelength spacing.
        # First need to pad to an integer of 10 by adding NaNs.
        if len(new_wls) % 10 != 0:
            n_pad = 10 - (len(new_wls) % 10)
            new_wls.extend([numpy.nan]*n_pad)
            new_fls.extend([numpy.nan]*n_pad)
        binned_sub_wl = numpy.nanmean(numpy.asarray(new_wls).reshape(-1, 10),
                                      axis=1)
        binned_sub_fl = numpy.nanmean(numpy.asarray(new_fls).reshape(-1, 10),
                                      axis=1)
        binned_wls.extend(binned_sub_wl)
        binned_fls.extend(binned_sub_fl)
        # Update where the next sub_spectrum starts.
        prev_index = gap_ind+1

    # If the last gap did not cover to the end of the spectrum, do one more
    # subsection.
    if prev_index < len(wls):
        # Get interpolated spectrum for the final subsection.
        new_wls, new_fls = interpolate_subspec(wls, fls, prev_index, len(wls),
                                               wl_step)
        # Push the interpolated values into the list via extension, but only if
        # it is to be plotted.
        if showplot:
            interpolated_wls.extend(new_wls)
            interpolated_fls.extend(new_fls)
        # Now bin the spectrum down by a factor of 10 in resolution to our
        # desired wavelength spacing.
        # First need to pad to an integer of 10 by adding NaNs.
        if len(new_wls) % 10 != 0:
            n_pad = 10 - (len(new_wls) % 10)
            new_wls.extend([numpy.nan]*n_pad)
            new_fls.extend([numpy.nan]*n_pad)
        binned_sub_wl = numpy.nanmean(numpy.asarray(new_wls).reshape(-1, 10),
                                      axis=1)
        binned_sub_fl = numpy.nanmean(numpy.asarray(new_fls).reshape(-1, 10),
                                      axis=1)
        binned_wls.extend(binned_sub_wl)
        binned_fls.extend(binned_sub_fl)

    # Show the plotted spectra if requested.
    if showplot:
        import matplotlib.pyplot as pyp
        pyp.plot(wls, fls, '-ko')
        # Uncomment the lines below to overplot the (oversampled) interpolated
        # spectrum.
        #if showplot:
        #    pyp.plot(interpolated_wls, interpolated_fls, '-ro')
        pyp.plot(binned_wls, binned_fls, '-go')
        for gapmark_ind in wl_gaps:
            pyp.axvline(wls[gapmark_ind])
        pyp.show()
    return zip(binned_wls, binned_fls)
#--------------------

#--------------------
def get_data_iue(obsid, filt):
    """
    Given an IUE observation ID, returns the spectral data.  Note that, in some
    cases, an observation ID has both a low and high dispersion spectrum
    available.  In that event, both the low and high dispersion spectra are
    returned as data series, regardless of whether the user wanted one or both.

    :param obsid: The IUE observation ID to retrieve the data from.

    :type obsid: str

    :param filt: The filter for this IUE observation ID.  It must be either
    "LOW_DISP" or "HIGH_DISP".

    :type filt: str

    :returns: JSON -- The spectral data for this observation ID.

    Error codes:
    From parse_obsid_iue:
    0 = No error parsing observation ID.
    1 = Observation ID does not begin with expected first three letters.
    2 = No mxlo or mxhi file found on disk.
    From this module:
    3 = Could not open one or more FITS file for reading.
    4 = Filter value is not an accepted value.
    """

    # This error code will be used unless there's a problem reading any
    # of the FITS files in the list, or the FILTER value is not understood.
    errcode = 0

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For IUE, this defines the x-axis and y-axis units as a string.
    iue_xunit = "Angstroms (vacuum, heliocentric)"
    iue_yunit = "ergs/cm^2/s/Angstrom"

    # Parse the obsID string to determine the paths+files to read.  Note:
    # this step will assign some of the error codes returned to the top level.
    if filt == ' ':
        filt = "UNKNOWN"
    if filt.upper() in ["LOW_DISP", "HIGH_DISP"] or filt == "UNKNOWN":
        parsed_files_result = parse_obsid_iue(obsid, filt.upper())
        errcode = parsed_files_result.errcode
    else:
        errcode = 4

    # In the case of low dispersion spectra, there can be two apertures for
    # a single obsID.  In that case, we return a list of TWO DataSeries, one
    # for each aperture.  In other words, we treat the single obsID as if it
    # were two different obsIDs in the case of a double-aperture.
    all_data_series = []

    # For each file, read in the contents and create a return JSON object.
    if errcode == 0:
        for sfile in parsed_files_result.specfiles:
            # Figure out if this is an mxhi or mxlo spectrum.
            if sfile[-7:] == "mxlo.gz":
                is_lo = True
                is_hi = False
            else:
                is_lo = False
                is_hi = True

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
                                # Create the return DataSeries object.
                                all_data_series.append(
                                    DataSeries('iue', obsid,
                                               [[data_point(x=x, y=y) for x, y
                                                 in wlfls]],
                                               ['IUE_' + obsid + ' DISP:'
                                                + dispersion + ' APER:' +
                                                apertures[aper]],
                                               [iue_xunit], [iue_yunit],
                                               errcode))

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
                                order_spec = {'order':orders[order],
                                              'wls':numpy.asarray(wls),
                                              'fls':numpy.asarray(fls)}
                                order_spectra.append(order_spec)

                        # Order-combine the spectra.
                        comb_spec = order_combine(order_spectra, camera, False)

                        # Resample onto an evenly-spaced wavelength scale.
                        comb_spec_reb = resample_spectrum(comb_spec, camera,
                                                          False)

                        # Create the return DataSeries object.
                        all_data_series.append(
                            DataSeries('iue', obsid,
                                       [[data_point(x=x, y=y) for x, y
                                         in comb_spec_reb]],
                                       ['IUE_' + obsid + ' DISP:'
                                        + dispersion + ' APER:' +
                                        aperture],
                                       [iue_xunit], [iue_yunit],
                                       errcode))

            except IOError:
                errcode = 3
                all_data_series.append(
                    DataSeries('iue', obsid, [], [''], [''], [''], errcode))

    else:
        # This is where an error DataSeries object would be returned.
        all_data_series.append(
            DataSeries('iue', obsid, [], [], [],
                       [], errcode))

    # Return the DataSeries object back to the calling module.
    if len(all_data_series) == 1:
        return all_data_series[0]
    else:
        return all_data_series
#--------------------
