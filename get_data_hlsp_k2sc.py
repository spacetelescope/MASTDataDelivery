"""
.. module:: get_data_hlsp_k2sc

   :synopsis: Returns K2SC lightcurve data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
from astropy.io import fits
from data_series import DataSeries
from parse_obsid_hlsp_k2sc import parse_obsid_hlsp_k2sc

#--------------------
def get_data_hlsp_k2sc(obsid):
    """
    Given a K2SC observation ID, returns the lightcurve data.

    :param obsid: The K2SC observation ID to retrieve the data from.

    :type obsid: str

    :returns: JSON -- The lightcurve data for this observation ID.

    Error codes:
    From parse_obsid_hlsp_k2sc:
    0 = No error.
    1 = Error parsing K2SC observation ID.
    2 = Cadence not recognized as long cadence.
    3 = File is missing on disk.
    From this module:
    4 = FITS file does not have the expected number of FITS extensions.
    5 = Could not open FITS file for reading.
    """

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For K2SC, this defines the x-axis and y-axis units as a string.
    k2sc_xunit = "BJD"
    k2sc_yunit = "electrons / second"

    # Parse the obsID string to determine the paths+files to read.  Note:
    # this step will assign some of the error codes returned to the top level.
    parsed_file_result = parse_obsid_hlsp_k2sc(obsid)

    if parsed_file_result.errcode == 0:
        # For each file, read in the contents and create a return JSON object.
        all_plot_labels = ['']*2*len(parsed_file_result.files)
        all_plot_series = ['']*2*len(parsed_file_result.files)
        all_plot_xunits = ['']*2*len(parsed_file_result.files)
        all_plot_yunits = ['']*2*len(parsed_file_result.files)

        # This error code will be used unless there's a problem reading any of
        # the FITS files in the list.
        errcode = 0
        for i, kfile in enumerate(parsed_file_result.files):
            try:
                with fits.open(kfile) as hdulist:
                    # Extract time stamps and relevant fluxes.  Note that for
                    # K2SC there are 2 relevant extensions.  The first
                    # extension is the detrended PDCSAP lightcurve, the second
                    # is the detrended SAP lightcurve.
                    if len(hdulist) == 3:
                        for j in xrange(1, 3):
                            # Extension name.
                            extname = hdulist[j].header["EXTNAME"].strip()

                            # Timestamps.
                            bjd = [float("{0:.8f}".format(
                                x + 2454833.0)) for x in
                                   hdulist[j].data["time"]]

                            # Corrected flux.
                            cor_flux = [float("{0:.8f}".format(x)) for x in
                                        hdulist[j].data["flux"]]

                            # Create the plot label and plot series for the
                            # extracted and detrended fluxes.
                            this_plot_label = (
                                'K2SC_' + parsed_file_result.k2scid + ' ' +
                                parsed_file_result.campaign.upper() + ' ' +
                                extname)

                            # Note that the indexes are (j-1) since j loops
                            # over the extension number, but the lists are
                            # zero-indexed, so "k" is the insert index.
                            k = j-1
                            all_plot_labels[k] = this_plot_label
                            all_plot_series[k] = [data_point(x=x, y=y) for
                                                  x, y in zip(bjd, cor_flux)]
                            all_plot_xunits[k] = k2sc_xunit
                            all_plot_yunits[k] = k2sc_yunit
                    else:
                        # Then there aren't the expected number of extensions.
                        errcode = 4
            except IOError:
                errcode = 5
                all_plot_labels[i] = ''
                all_plot_series[i] = []
                all_plot_xunits[i] = ''
                all_plot_yunits[i] = ''

        # Create the return DataSeries object.
        return_dataseries = DataSeries('hlsp_k2sc', obsid, all_plot_series,
                                       all_plot_labels,
                                       all_plot_xunits, all_plot_yunits,
                                       errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries('hlsp_k2sc', obsid, [], [], [], [],
                                       parsed_file_result.errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
