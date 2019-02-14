"""
.. module:: get_data_hlsp_polar

   :synopsis: Returns POLAR lightcurve data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import numpy
from astropy.io import fits
from .data_series import DataSeries
from .parse_obsid_hlsp_polar import parse_obsid_hlsp_polar

#--------------------
def get_data_hlsp_polar(obsid, hlsps_dir):
    """
    Given a POLAR observation ID, returns the lightcurve data.

    :param obsid: The POLAR observation ID to retrieve the data from.

    :type obsid: str

    :param hlsps_dir: The path to the directory containing the "hlsps/"
    folder with the data files.

    :type hlsps_dir: str

    :returns: JSON -- The lightcurve data for this observation ID.

    Error codes:
    From parse_obsid_hlsp_polar:
    0 = No error.
    1 = Error parsing POLAR observation ID.
    2 = Cadence not recognized as long cadence.
    3 = File is missing on disk.
    From this module:
    4 = FITS file does not have the expected number of FITS extensions.
    5 = Could not open FITS file for reading.
    6 = All values were non-finite in x and/or y.
    """

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For POLAR, this defines the x-axis and y-axis units as a string.
    polar_xunit = "BJD"
    polar_yunit = "normalized"

    # Parse the obsID string to determine the paths+files to read.  Note:
    # this step will assign some of the error codes returned to the top level.
    parsed_file_result = parse_obsid_hlsp_polar(obsid, hlsps_dir)

    if parsed_file_result.errcode == 0:
        # For each file, read in the contents and create a return JSON object.
        all_plot_labels = ['']*2*len(parsed_file_result.files)
        all_plot_series = ['']*2*len(parsed_file_result.files)
        all_plot_xunits = ['']*2*len(parsed_file_result.files)
        all_plot_yunits = ['']*2*len(parsed_file_result.files)

        # This error code will be used unless there's a problem reading any of
        # the FITS files in the list.
        errcode = 0
        for kfile in parsed_file_result.files:
            try:
                with fits.open(kfile) as hdulist:
                    # Extract time stamps and relevant fluxes.
                    if len(hdulist) == 3:
                        # Filtered timestamps.
                        fil_bjd = (hdulist[1].data["FILTIME"] + 2400000.0)
                        # Filtered flux.
                        fil_flux = hdulist[1].data["FILFLUX"]

                        # Detrended timestamps.
                        det_bjd = (hdulist[2].data["DETTIME"] + 2400000.0)
                        # Detrended flux.
                        det_flux = hdulist[2].data["DETFLUX"]

                        # Only keep those points that don't have NaN's in them.
                        det_where_keep = numpy.where(
                            (numpy.isfinite(det_bjd)) &
                            (numpy.isfinite(det_flux)))[0]
                        if det_where_keep.size > 0:
                            det_bjd = det_bjd[det_where_keep]
                            det_flux = det_flux[det_where_keep]
                        else:
                            errcode = 6

                        fil_where_keep = numpy.where(
                            (numpy.isfinite(fil_bjd)) &
                            (numpy.isfinite(fil_flux)))[0]
                        if fil_where_keep.size > 0:
                            fil_bjd = fil_bjd[fil_where_keep]
                            fil_flux = fil_flux[fil_where_keep]
                        else:
                            errcode = 6

                        # Create the plot label and plot series for the
                        # extracted and detrended fluxes.
                        this_plot_label = (
                            'POLAR_' + parsed_file_result.polarid +
                            ' ' + parsed_file_result.campaign.upper())

                        if errcode == 0:
                            # Get arrays into regular list with decimal limits.
                            det_bjd = [float("{0:.8f}".format(x))
                                       for x in det_bjd]
                            fil_bjd = [float("{0:.8f}".format(x))
                                       for x in fil_bjd]
                            det_flux = [float("{0:.8f}".format(x))
                                        for x in det_flux]
                            fil_flux = [float("{0:.8f}".format(x))
                                        for x in fil_flux]
                            all_plot_labels[0] = (this_plot_label +
                                                  ' Detrended')
                            all_plot_series[0] = [data_point(x=x, y=y) for
                                                  x, y in zip(det_bjd,
                                                              det_flux)]
                            all_plot_xunits[0] = polar_xunit
                            all_plot_yunits[0] = polar_yunit
                            all_plot_labels[1] = (this_plot_label +
                                                  ' Det.+Filtered')
                            all_plot_series[1] = [data_point(x=x, y=y) for
                                                  x, y in zip(fil_bjd,
                                                              fil_flux)]
                            all_plot_xunits[1] = polar_xunit
                            all_plot_yunits[1] = polar_yunit
                        else:
                            all_plot_labels[0] = ''
                            all_plot_series[0] = []
                            all_plot_xunits[0] = ''
                            all_plot_yunits[0] = ''
                            all_plot_labels[1] = ''
                            all_plot_series[1] = []
                            all_plot_xunits[1] = ''
                            all_plot_yunits[1] = ''
                    else:
                        # Then there aren't the expected number of extensions.
                        errcode = 4
            except IOError:
                errcode = 5
                all_plot_labels[0] = ''
                all_plot_series[0] = []
                all_plot_xunits[0] = ''
                all_plot_yunits[0] = ''
                all_plot_labels[1] = ''
                all_plot_series[1] = []
                all_plot_xunits[1] = ''
                all_plot_yunits[1] = ''

        # Create the return DataSeries object.
        return_dataseries = DataSeries('hlsp_polar', obsid, all_plot_series,
                                       all_plot_labels,
                                       all_plot_xunits, all_plot_yunits,
                                       errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries('hlsp_polar', obsid, [], [], [], [],
                                       parsed_file_result.errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
