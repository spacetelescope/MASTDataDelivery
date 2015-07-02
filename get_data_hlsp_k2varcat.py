"""
.. module:: get_data_hlsp_k2varcat

   :synopsis: Returns K2VARCAT lightcurve data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

from astropy.io import fits
import collections
from data_series import DataSeries
from parse_obsid_hlsp_k2varcat import parse_obsid_hlsp_k2varcat
import re

#--------------------
def get_data_hlsp_k2varcat(obsid):
    """
    Given a K2VARCAT observation ID, returns the lightcurve data.

    :param obsid: The K2VARCAT observation ID to retrieve the data from.

    :type obsid: str

    :returns: JSON -- The lightcurve data for this observation ID.

    Error codes:
    From parse_obsid_hlsp_k2varcat:
    0 = No error.
    1 = Error parsing K2VARCAT observation ID.
    2 = Cadence not recognized as long cadence.
    3 = File is missing on disk.
    From this module:
    4 = BJD reference date not expected value.
    5 = Could not open FITS file for reading.
    """

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For K2VARCAT, this defines the x-axis and y-axis units as a string.
    k2varcat_xunit = "BJD"
    k2varcat_detrended_yunit = "normalized"
    k2varcat_extracted_yunit = "electrons / second"

    # Parse the obsID string to determine the paths+files to read.  Note:
    # this step will assign some of the error codes returned to the top level.
    parsed_file_result = parse_obsid_hlsp_k2varcat(obsid)

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
                    # Extract time stamps and relevant fluxes.
                    tunit = hdulist[1].header["TUNIT1"]
                    bjd_ref_str = re.split('-', tunit)[1].strip()
                    if bjd_ref_str == "2454833":
                        bjd_ref = float(bjd_ref_str)
                        bjd = [bjd_ref + float(x) for x in
                               hdulist[1].data["TIME"]]
                        # Extracted (not detrended) flux.
                        ext_flux = [float(x) for x in
                                    hdulist[1].data["APTFLUX"]]
                        # Extracted (and detrended) flux.
                        det_flux = [float(x) for x in
                                    hdulist[1].data["DETFLUX"]]

                        # Create the plot label and plot series for the
                        # extracted and detrended fluxes.
                        this_plot_label = ('K2VARCAT_' +
                                           parsed_file_result.k2varcatid +
                                           ' ' +
                                           parsed_file_result.campaign.upper())
                        all_plot_labels[i*2] = this_plot_label + ' Extracted'
                        all_plot_series[i*2] = [data_point(x=x, y=y) for
                                                x, y in zip(bjd, ext_flux)]
                        all_plot_xunits[i*2] = k2varcat_xunit
                        all_plot_yunits[i*2] = k2varcat_extracted_yunit
                        all_plot_labels[i*2+1] = this_plot_label + ' Detrended'
                        all_plot_series[i*2+1] = [data_point(x=x, y=y) for
                                                  x, y in zip(bjd, det_flux)]
                        all_plot_xunits[i*2+1] = k2varcat_xunit
                        all_plot_yunits[i*2+1] = k2varcat_detrended_yunit
                    else:
                        # Then BJD reference was not the expected value.
                        errcode = 4
                        all_plot_labels[i*2] = ''
                        all_plot_series[i*2] = []
                        all_plot_xunits[i*2] = ''
                        all_plot_yunits[i*2] = ''
                        all_plot_labels[i*2+1] = ''
                        all_plot_series[i*2+1] = []
                        all_plot_xunits[i*2+1] = ''
                        all_plot_yunits[i*2+1] = ''
            except IOError:
                errcode = 5
                all_plot_labels[i*2] = ''
                all_plot_series[i*2] = []
                all_plot_xunits[i*2] = ''
                all_plot_yunits[i*2] = ''
                all_plot_labels[i*2+1] = ''
                all_plot_series[i*2+1] = []
                all_plot_xunits[i*2+1] = ''
                all_plot_yunits[i*2+1] = ''

        # Create the return DataSeries object.
        return_dataseries = DataSeries('hlsp_k2varcat', obsid, all_plot_series,
                                       all_plot_labels,
                                       all_plot_xunits, all_plot_yunits,
                                       errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries('hlsp_k2varcat', obsid, [], [], [], [],
                                       parsed_file_result.errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
