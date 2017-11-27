"""
.. module:: get_data_hlsp_k2sff

   :synopsis: Returns K2SFF lightcurve data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

from astropy.io import fits
import collections
from data_series import DataSeries
from parse_obsid_hlsp_k2sff import parse_obsid_hlsp_k2sff

#--------------------
def get_data_hlsp_k2sff(obsid):
    """
    Given a K2SFF observation ID, returns the lightcurve data.

    :param obsid: The K2SFF observation ID to retrieve the data from.

    :type obsid: str

    :returns: JSON -- The lightcurve data for this observation ID.

    Error codes:
    From parse_obsid_hlsp_k2sff:
    0 = No error.
    1 = Error parsing K2SFF observation ID.
    2 = Cadence not recognized as long cadence.
    3 = File is missing on disk.
    From this module:
    4 = FITS file does not have the expected number of FITS extensions.
    5 = Could not open FITS file for reading.
    """

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For K2SFF, this defines the x-axis and y-axis units as a string.
    k2sff_xunit = "BJD"
    k2sff_yunit = "normalized"

    # Parse the obsID string to determine the paths+files to read.  Note:
    # this step will assign some of the error codes returned to the top level.
    parsed_file_result = parse_obsid_hlsp_k2sff(obsid)

    if parsed_file_result.errcode == 0:
        # For each file, read in the contents and create a return JSON object.
        all_plot_labels = ['']*42*len(parsed_file_result.files)
        all_plot_series = ['']*42*len(parsed_file_result.files)
        all_plot_xunits = ['']*42*len(parsed_file_result.files)
        all_plot_yunits = ['']*42*len(parsed_file_result.files)

        # This error code will be used unless there's a problem reading any of
        # the FITS files in the list.
        errcode = 0
        for i, kfile in enumerate(parsed_file_result.files):
            try:
                with fits.open(kfile) as hdulist:
                    # Extract time stamps and relevant fluxes.  Note that for
                    # K2SFF there are 21 relevant extensions, and two fluxes
                    # (raw and detrended) for each.  The first extension is the
                    # "best" aperture from the 20, then 2 - 21 are the 20 used.
                    if len(hdulist) == 25:
                        for j in xrange(1, 22):
                            # Extension name.
                            extname = hdulist[j].header["EXTNAME"].strip()

                            # Timestamps.
                            bjdreff = hdulist[j].header["BJDREFF"]
                            bjdrefi = hdulist[j].header["BJDREFI"]
                            bjd = [float("{0:.8f}".format(
                                x + bjdreff + bjdrefi)) for x in
                                   hdulist[j].data["T"]]

                            # Raw flux.
                            raw_flux = [float("{0:.8f}".format(x)) for x in
                                        hdulist[j].data["FRAW"]]
                            # Corrected flux.
                            cor_flux = [float("{0:.8f}".format(x)) for x in
                                        hdulist[j].data["FCOR"]]

                            # Create the plot label and plot series for the
                            # extracted and detrended fluxes.
                            this_plot_label = (
                                'K2SFF_' + parsed_file_result.k2sffid + ' ' +
                                parsed_file_result.campaign.upper() + ' ' +
                                extname)

                            # Note that the indexes are (j-1) since j loops
                            # over the extension number, but the lists are
                            # zero-indexed, so "k" is the insert index.
                            k = j-1
                            all_plot_labels[k*2] = (this_plot_label +
                                                    ' Raw')
                            all_plot_series[k*2] = [data_point(x=x, y=y) for
                                                    x, y in zip(bjd, raw_flux)]
                            all_plot_xunits[k*2] = k2sff_xunit
                            all_plot_yunits[k*2] = k2sff_yunit
                            all_plot_labels[k*2+1] = (this_plot_label +
                                                      ' Corrected')
                            all_plot_series[k*2+1] = [data_point(x=x, y=y) for
                                                      x, y in zip(bjd,
                                                                  cor_flux)]
                            all_plot_xunits[k*2+1] = k2sff_xunit
                            all_plot_yunits[k*2+1] = k2sff_yunit
                    else:
                        # Then there aren't the expected number of extensions.
                        errcode = 4
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
        return_dataseries = DataSeries('hlsp_k2sff', obsid, all_plot_series,
                                       all_plot_labels,
                                       all_plot_xunits, all_plot_yunits,
                                       errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries('hlsp_k2sff', obsid, [], [], [], [],
                                       parsed_file_result.errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
