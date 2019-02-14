"""
.. module:: get_data_hlsp_k2gap

   :synopsis: Returns K2GAP lightcurve data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import numpy
from .data_series import DataSeries
from .parse_obsid_hlsp_k2gap import parse_obsid_hlsp_k2gap

#--------------------
def get_data_hlsp_k2gap(obsid, hlsps_dir):
    """
    Given a K2GAP observation ID, returns the lightcurve data.

    :param obsid: The K2GAP observation ID to retrieve the data from.

    :type obsid: str

    :param hlsps_dir: The path to the directory containing the "hlsps/"
    folder with the data files.

    :type hlsps_dir: str

    :returns: JSON -- The lightcurve data for this observation ID.

    Error codes:
    From parse_obsid_hlsp_k2gap:
    0 = No error.
    1 = Error parsing K2GAP observation ID.
    2 = Cadence not recognized as long cadence.
    3 = File is missing on disk.
    """

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For K2GAP, this defines the x-axis and y-axis units as a string.
    k2gap_xunit = "BJD"
    k2gap_yunit = "normalized"

    # Parse the obsID string to determine the paths+files to read.  Note:
    # this step will assign some of the error codes returned to the top level.
    parsed_file_result = parse_obsid_hlsp_k2gap(obsid, hlsps_dir)

    if parsed_file_result.errcode == 0:
        # For each file, read in the contents and create a return JSON object.
        all_plot_labels = ['']*len(parsed_file_result.files)
        all_plot_series = ['']*len(parsed_file_result.files)
        all_plot_xunits = ['']*len(parsed_file_result.files)
        all_plot_yunits = ['']*len(parsed_file_result.files)

        # This error code will be used unless there's a problem reading any of
        # the FITS files in the list.
        errcode = 0
        for i, kfile in enumerate(parsed_file_result.files):
            kepbjds, cor_flux = numpy.genfromtxt(kfile, comments='#',
                                                 unpack=True)

            bjd = [float("{0:.8f}".format(x + 2454833.0)) for x in kepbjds]
            cor_flux = [float("{0:.8f}".format(x)) for x in cor_flux]

            # Create the plot label and plot series for the
            # extracted and detrended fluxes.
            this_plot_label = (
                'K2GAP_' + parsed_file_result.k2gapid + ' ' +
                parsed_file_result.campaign.upper())
            all_plot_labels[i] = this_plot_label
            all_plot_series[i] = [data_point(x=x, y=y) for
                                  x, y in zip(bjd, cor_flux)]
            all_plot_xunits[i] = k2gap_xunit
            all_plot_yunits[i] = k2gap_yunit

        # Create the return DataSeries object.
        return_dataseries = DataSeries('hlsp_k2gap', obsid, all_plot_series,
                                       all_plot_labels,
                                       all_plot_xunits, all_plot_yunits,
                                       errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries('hlsp_k2gap', obsid, [], [], [], [],
                                       parsed_file_result.errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
