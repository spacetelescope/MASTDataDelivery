"""
.. module:: mpl_get_data_wuppe

   :synopsis: Returns WUPPE spectral data as a JSON string through Randy's
   mast_plot.pl service.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
from data_series import DataSeries
from operator import itemgetter
import requests

#--------------------
def mpl_get_data_wuppe(obsid):
    """
    Given a WUPPE observation ID, returns the spectral data.

    :param obsid: The WUPPE observation ID to retrieve the data from.

    :type obsid: str

    :returns: JSON -- The spectral data for this observation ID.

    Error codes:
    0 = No error.
    1 = HTTP Error 500 code returned.
    2 = "File not found error" returned by mast_plot.pl.
    3 = Wavelength and/or flux arrays are zero length.
    4 = Wavelength and flux arrays are not of equal length.
    """

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For WUPPE, this defines the x-axis and y-axis units as a string.
    wuppe_xunit = "Angstroms"
    wuppe_yunit = "ergs/cm^2/s/Angstrom"

    # Initiate a reqest from Randy's perl script service.  Note the return is
    # a 3-element list, each element itself if a list containing another list.
    return_request = requests.get("https://archive.stsci.edu/cgi-bin/mast_plot"
                                  ".pl?WUPPE=" + obsid.lower())

    if return_request.status_code == 500:
        # If an HTTP 500 error is returned, catch it here, since it can't
        # be converted to a JSON string using the built-in json().
        errcode = 1
        return_dataseries = DataSeries('wuppe', obsid, [], [], [], [], errcode)
    else:
        return_request = return_request.json()

        if len(return_request[0]) == 0:
            # File not found by service.
            errcode = 2
            return_dataseries = DataSeries('wuppe', obsid, [], [], [], [],
                                           errcode)
        else:
            # Wavelengths are the first list in the returned 3-element list.
            wls = [float(x) for x in return_request[0][0]]

            # Fluxes are the second list in the returned 3-element list.
            fls = [float(x) for x in return_request[1][0]]

            # This error code will be used unless there's a problem reading any
            # of the FITS files in the list.
            errcode = 0

            # Make sure wavelengths and fluxes are not empty and are same size.
            if len(wls) > 0 and len(fls) > 0 and len(wls) == len(fls):

                # Make sure wavelengths and fluxes are sorted
                # from smallest wavelength to largest.
                sort_indexes = [x[0] for x in sorted(enumerate(wls),
                                                     key=itemgetter(1))]
                wls = [wls[x] for x in sort_indexes]
                fls = [fls[x] for x in sort_indexes]

                # Zip the wavelengths and fluxes into tuples to create the plot
                # series.
                plot_series = [[data_point(x=x, y=y) for x, y in zip(wls, fls)]]

                # Create the return DataSeries object.
                return_dataseries = DataSeries('wuppe', obsid, plot_series,
                                               ['WUPPE_' + obsid],
                                               [wuppe_xunit], [wuppe_yunit],
                                               errcode)
            elif len(wls) == 0 or len(fls) == 0:
                errcode = 3
                return_dataseries = DataSeries('wuppe', obsid, [], [], [], [],
                                               errcode)
            else:
                errcode = 4
                return_dataseries = DataSeries('wuppe', obsid, [], [], [], [],
                                               errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
