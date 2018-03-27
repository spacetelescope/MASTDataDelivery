"""
.. module:: get_data_hlsp_everest

   :synopsis: Returns EVEREST lightcurve data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import numpy
from astropy.io import fits
from data_series import DataSeries
from parse_obsid_hlsp_everest import parse_obsid_hlsp_everest

#--------------------
def get_data_hlsp_everest(obsid):
    """
    Given a EVEREST observation ID, returns the lightcurve data.

    :param obsid: The EVEREST observation ID to retrieve the data from.

    :type obsid: str

    :returns: JSON -- The lightcurve data for this observation ID.

    Error codes:
    From parse_obsid_hlsp_everest:
    0 = No error.
    1 = Error parsing EVEREST observation ID.
    2 = Cadence not recognized as long cadence.
    3 = File is missing on disk.
    From this module:
    4 = FITS file does not have the expected number of FITS extensions.
    5 = Could not open FITS file for reading.
    6 = All values were non-finite in x and/or y.
    """

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For EVEREST, this defines the x-axis and y-axis units as a string.
    everest_xunit = "BJD"
    everest_yunit = "electrons / second"

    # Parse the obsID string to determine the paths+files to read.  Note:
    # this step will assign some of the error codes returned to the top level.
    parsed_file_result = parse_obsid_hlsp_everest(obsid)

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
                    if len(hdulist) == 6:
                        # Timestamps.
                        bjd = (hdulist[1].data["TIME"] +
                               hdulist[1].header["BJDREFF"] +
                               hdulist[1].header["BJDREFI"])
                        # Raw flux.
                        raw_flux = hdulist[1].data["FRAW"]
                        # Corrected flux.
                        cor_flux = hdulist[1].data["FCOR"]
                        # Only keep those points that don't have NaN's in them.
                        where_keep = numpy.where(
                            (numpy.isfinite(bjd)) &
                            (numpy.isfinite(raw_flux)) &
                            (numpy.isfinite(cor_flux)))[0]
                        if where_keep.size > 0:
                            bjd = bjd[where_keep]
                            raw_flux = raw_flux[where_keep]
                            cor_flux = cor_flux[where_keep]
                        else:
                            errcode = 6

                        # Create the plot label and plot series for the
                        # extracted and detrended fluxes.
                        this_plot_label = (
                            'EVEREST_' + parsed_file_result.everestid +
                            ' ' + parsed_file_result.campaign.upper())

                        if errcode == 0:
                            # Get arrays into regular list with decimal limits.
                            bjd = [float("{0:.8f}".format(x)) for x in bjd]
                            raw_flux = [float("{0:.8f}".format(x))
                                        for x in raw_flux]
                            cor_flux = [float("{0:.8f}".format(x))
                                        for x in cor_flux]
                            all_plot_labels[0] = (this_plot_label +
                                                  ' Raw')
                            all_plot_series[0] = [data_point(x=x, y=y) for
                                                  x, y in zip(bjd, raw_flux)]
                            all_plot_xunits[0] = everest_xunit
                            all_plot_yunits[0] = everest_yunit
                            all_plot_labels[1] = (this_plot_label +
                                                  ' Corrected')
                            all_plot_series[1] = [data_point(x=x, y=y) for
                                                  x, y in zip(bjd,
                                                              cor_flux)]
                            all_plot_xunits[1] = everest_xunit
                            all_plot_yunits[1] = everest_yunit
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
        return_dataseries = DataSeries('hlsp_everest', obsid, all_plot_series,
                                       all_plot_labels,
                                       all_plot_xunits, all_plot_yunits,
                                       errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries('hlsp_everest', obsid, [], [], [], [],
                                       parsed_file_result.errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
