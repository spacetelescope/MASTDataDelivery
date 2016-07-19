"""
.. module:: get_data_hlsp_k2everest

   :synopsis: Returns K2EVEREST lightcurve data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
from astropy.io import fits
from data_series import DataSeries
from parse_obsid_hlsp_k2everest import parse_obsid_hlsp_k2everest

#--------------------
def get_data_hlsp_k2everest(obsid):
    """
    Given a K2EVEREST observation ID, returns the lightcurve data.

    :param obsid: The K2EVEREST observation ID to retrieve the data from.

    :type obsid: str

    :returns: JSON -- The lightcurve data for this observation ID.

    Error codes:
    From parse_obsid_hlsp_k2everest:
    0 = No error.
    1 = Error parsing K2EVEREST observation ID.
    2 = Cadence not recognized as long cadence.
    3 = File is missing on disk.
    From this module:
    4 = FITS file does not have the expected number of FITS extensions.
    5 = Could not open FITS file for reading.
    """

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For K2EVEREST, this defines the x-axis and y-axis units as a string.
    k2everest_xunit = "BJD"
    k2everest_yunit = "electrons / second"

    # Parse the obsID string to determine the paths+files to read.  Note:
    # this step will assign some of the error codes returned to the top level.
    parsed_file_result = parse_obsid_hlsp_k2everest(obsid)

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
                    # Extract time stamps and relevant fluxes.  Note that for
                    # K2EVEREST there are 21 relevant extensions, and two fluxes
                    # (raw and detrended) for each.  The first extension is the
                    # "best" aperture from the 20, then 2 - 21 are the 20 used.
                    if len(hdulist) == 5:
                        # Timestamps.
                        bjd = [float(x) for x in
                               (float(hdulist[1].header["BJDREFI"]) +
                                hdulist[1].header["BJDREFF"] +
                                hdulist[1].data["TIME"])]

                        # Raw flux.
                        raw_flux = [float("{0:.8f}".format(x)) for x in
                                    hdulist[1].data["RAW_FLUX"]]
                        # Corrected flux.
                        cor_flux = [float("{0:.8f}".format(x)) for x in
                                    hdulist[1].data["FLUX"]]

                        # Create the plot label and plot series for the
                        # extracted and detrended fluxes.
                        this_plot_label = (
                            'K2EVEREST_' + parsed_file_result.k2everestid +
                            ' ' + parsed_file_result.campaign.upper())

                        # Note that the indexes are (j-1) since j loops
                        # over the extension number, but the lists are
                        # zero-indexed, so "k" is the insert index.
                        all_plot_labels[0] = (this_plot_label +
                                              ' Raw')
                        all_plot_series[0] = [data_point(x=x, y=y) for
                                              x, y in zip(bjd, raw_flux)]
                        all_plot_xunits[0] = k2everest_xunit
                        all_plot_yunits[0] = k2everest_yunit
                        all_plot_labels[1] = (this_plot_label +
                                              ' Corrected')
                        all_plot_series[1] = [data_point(x=x, y=y) for
                                              x, y in zip(bjd,
                                                          cor_flux)]
                        all_plot_xunits[1] = k2everest_xunit
                        all_plot_yunits[1] = k2everest_yunit
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
        return_dataseries = DataSeries('hlsp_k2everest', obsid, all_plot_series,
                                       all_plot_labels,
                                       all_plot_xunits, all_plot_yunits,
                                       errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries('hlsp_k2everest', obsid, [], [], [], [],
                                       parsed_file_result.errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
