"""
.. module:: get_data_k2

   :synopsis: Returns K2 lightcurve data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

from astropy.io import fits
from data_series import DataSeries
from parse_obsid_k2 import parse_obsid_k2

#--------------------
def get_data_k2(obsid):
    """
    Given a K2 observation ID, returns the lightcurve data.

    :param obsid: The K2 observation ID to retrieve the data from.

    :type obsid: str

    :returns: JSON -- The lightcurve data for this observation ID.

    Error codes:
    From parse_obsid_k2:
    0 = No error.
    1 = Error parsing K2 observation ID.
    2 = Cadence not recognized as long cadence.
    3 = File is missing on disk.
    From this module:
    4 = Could not open FITS file for reading.
    """

    # For K2, this defines the x-axis and y-axis units as a string.
    k2_xunit = "BJD"
    k2_yunit = "electrons / second"

    # Parse the obsID string to determine the paths+files to read.  Note:
    # this step will assign some of the error codes returned to the top level.
    parsed_file_result = parse_obsid_k2(obsid)

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
                    # Extract time stamps and relevant fluxes.  Note that there
                    # are both PDCSAP and SAP fluxes returned.

                    # Extract time stamps and relevant fluxes.
                    bjd = [float(x) for x in
                           (float(hdulist[1].header["BJDREFI"]) +
                            hdulist[1].header["BJDREFF"] +
                            hdulist[1].data["TIME"])]
                    flux_sap = [float(x) for x in hdulist[1].data["SAP_FLUX"]]
                    flux_pdcsap = [float(x) for x in
                                   hdulist[1].data["PDCSAP_FLUX"]]

                    # Create the plot label and plot series for the
                    # extracted and detrended fluxes.
                    this_plot_label = ('KTWO_' + parsed_file_result.k2id +
                                       ' ' +
                                       parsed_file_result.campaign.upper())
                    all_plot_labels[i*2] = this_plot_label + ' SAP'
                    all_plot_series[i*2] = [x for x in
                                            zip(bjd, flux_sap)]
                    all_plot_xunits[i*2] = k2_xunit
                    all_plot_yunits[i*2] = k2_yunit

                    all_plot_labels[i*2+1] = this_plot_label + ' PDCSAP'
                    all_plot_series[i*2+1] = [x for x in
                                              zip(bjd, flux_pdcsap)]
                    all_plot_xunits[i*2+1] = k2_xunit
                    all_plot_yunits[i*2+1] = k2_yunit
            except IOError:
                errcode = 4
                all_plot_labels[i*2] = ''
                all_plot_series[i*2] = []
                all_plot_xunits[i*2] = ''
                all_plot_yunits[i*2] = ''
                all_plot_labels[i*2+1] = ''
                all_plot_series[i*2+1] = []
                all_plot_xunits[i*2+1] = ''
                all_plot_yunits[i*2+1] = ''

        # Create the return DataSeries object.
        return_dataseries = DataSeries('k2', obsid, all_plot_series,
                                       all_plot_labels,
                                       all_plot_xunits, all_plot_yunits,
                                       errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries('k2', obsid, [], [], [], [],
                                       parsed_file_result.errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
