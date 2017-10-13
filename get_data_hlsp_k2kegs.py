"""
.. module:: get_data_hlsp_k2kegs

   :synopsis: Returns K2KEGS lightcurve data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
from astropy.io import fits
from data_series import DataSeries
import numpy
from parse_obsid_hlsp_k2kegs import parse_obsid_hlsp_k2kegs

#--------------------
def get_data_hlsp_k2kegs(obsid):
    """
    Given a K2KEGS observation ID, returns the lightcurve data.

    :param obsid: The K2KEGS observation ID to retrieve the data from.

    :type obsid: str

    :returns: JSON -- The lightcurve data for this observation ID.

    Error codes:
    From parse_obsid_hlsp_k2kegs:
    0 = No error.
    1 = Error parsing K2KEGS observation ID.
    2 = Cadence not recognized as long cadence.
    3 = File is missing on disk.
    """

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For K2KEGS, this defines the x-axis and y-axis units as a string.
    k2kegs_xunit = "BJD"
    k2kegs_yunit = "counts/sec"

    # Parse the obsID string to determine the paths+files to read.  Note:
    # this step will assign some of the error codes returned to the top level.
    parsed_file_result = parse_obsid_hlsp_k2kegs(obsid)

    if parsed_file_result.errcode == 0:
        # For each file, read in the contents and create a return JSON object.
        all_plot_labels = ['']*6*len(parsed_file_result.files)
        all_plot_series = ['']*6*len(parsed_file_result.files)
        all_plot_xunits = ['']*6*len(parsed_file_result.files)
        all_plot_yunits = ['']*6*len(parsed_file_result.files)

        # This error code will be used unless there's a problem reading any of
        # the FITS files in the list.
        errcode = 0
        for i, kfile in enumerate(parsed_file_result.files):
            with fits.open(kfile) as hdulist:
                kepbjds = hdulist[1].data['TIME']
                fraw = hdulist[1].data['FRAW']
                fcor1 = hdulist[1].data['FCOR1']
                fcor2 = hdulist[1].data['FCOR2']
                fcor3 = hdulist[1].data['FCOR3']
                fcor4 = hdulist[1].data['FCOR4']
                fcor5 = hdulist[1].data['FCOR5']

            where_keep_1 = numpy.where((numpy.isfinite(kepbjds)) &
                                       (numpy.isfinite(fcor1)))
            where_keep_2 = numpy.where((numpy.isfinite(kepbjds)) &
                                       (numpy.isfinite(fcor2)))
            where_keep_3 = numpy.where((numpy.isfinite(kepbjds)) &
                                       (numpy.isfinite(fcor3)))
            where_keep_4 = numpy.where((numpy.isfinite(kepbjds)) &
                                       (numpy.isfinite(fcor4)))
            where_keep_5 = numpy.where((numpy.isfinite(kepbjds)) &
                                       (numpy.isfinite(fcor5)))
            where_keep_6 = numpy.where((numpy.isfinite(kepbjds)) &
                                       (numpy.isfinite(fraw)))

            bjd_1 = [float("{0:.8f}".format(x + 2454833.0))
                     for x in kepbjds[where_keep_1]]
            flux_1 = [float("{0:.8f}".format(x)) for x in fcor1[where_keep_1]]
            bjd_2 = [float("{0:.8f}".format(x + 2454833.0))
                     for x in kepbjds[where_keep_2]]
            flux_2 = [float("{0:.8f}".format(x)) for x in fcor2[where_keep_2]]
            bjd_3 = [float("{0:.8f}".format(x + 2454833.0))
                     for x in kepbjds[where_keep_3]]
            flux_3 = [float("{0:.8f}".format(x)) for x in fcor3[where_keep_3]]
            bjd_4 = [float("{0:.8f}".format(x + 2454833.0))
                     for x in kepbjds[where_keep_4]]
            flux_4 = [float("{0:.8f}".format(x)) for x in fcor4[where_keep_4]]
            bjd_5 = [float("{0:.8f}".format(x + 2454833.0))
                     for x in kepbjds[where_keep_5]]
            flux_5 = [float("{0:.8f}".format(x)) for x in fcor5[where_keep_5]]
            bjd_6 = [float("{0:.8f}".format(x + 2454833.0))
                     for x in kepbjds[where_keep_6]]
            flux_6 = [float("{0:.8f}".format(x)) for x in fraw[where_keep_6]]

            # Create the plot label and plot series for the
            # extracted and detrended fluxes.
            this_plot_label = (
                'KEGS_' + parsed_file_result.k2kegsid + ' ' +
                parsed_file_result.campaign.upper())
            all_plot_labels[i] = this_plot_label + ' FCOR1'
            all_plot_series[i] = [data_point(x=x, y=y) for
                                  x, y in zip(bjd_1, flux_1)]
            all_plot_xunits[i] = k2kegs_xunit
            all_plot_yunits[i] = k2kegs_yunit
            all_plot_labels[i+1] = this_plot_label + ' FCOR2'
            all_plot_series[i+1] = [data_point(x=x, y=y) for
                                    x, y in zip(bjd_2, flux_2)]
            all_plot_xunits[i+1] = k2kegs_xunit
            all_plot_yunits[i+1] = k2kegs_yunit
            all_plot_labels[i+2] = this_plot_label + ' FCOR3'
            all_plot_series[i+2] = [data_point(x=x, y=y) for
                                    x, y in zip(bjd_3, flux_3)]
            all_plot_xunits[i+2] = k2kegs_xunit
            all_plot_yunits[i+2] = k2kegs_yunit
            all_plot_labels[i+3] = this_plot_label + ' FCOR4'
            all_plot_series[i+3] = [data_point(x=x, y=y) for
                                    x, y in zip(bjd_4, flux_4)]
            all_plot_xunits[i+3] = k2kegs_xunit
            all_plot_yunits[i+3] = k2kegs_yunit
            all_plot_labels[i+4] = this_plot_label + ' FCOR5'
            all_plot_series[i+4] = [data_point(x=x, y=y) for
                                    x, y in zip(bjd_5, flux_5)]
            all_plot_xunits[i+4] = k2kegs_xunit
            all_plot_yunits[i+4] = k2kegs_yunit
            all_plot_labels[i+5] = this_plot_label + ' FRAW'
            all_plot_series[i+5] = [data_point(x=x, y=y) for
                                    x, y in zip(bjd_6, flux_6)]
            all_plot_xunits[i+5] = k2kegs_xunit
            all_plot_yunits[i+5] = k2kegs_yunit

        # Create the return DataSeries object.
        return_dataseries = DataSeries('hlsp_kegs', obsid, all_plot_series,
                                       all_plot_labels,
                                       all_plot_xunits, all_plot_yunits,
                                       errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries('hlsp_kegs', obsid, [], [], [], [],
                                       parsed_file_result.errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
