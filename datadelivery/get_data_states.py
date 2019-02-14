"""
.. module:: get_data_states

   :synopsis: Returns STATES spectral data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import numpy
from .data_series import DataSeries
from .parse_obsid_states import parse_obsid_states

#--------------------
def get_data_states(obsid, states_dir):
    """
    Given a STATES observation ID, returns the spectral data.

    :param obsid: The STATES observation ID to retrieve the data from.

    :type obsid: str

    :param states_dir: The path to the STATES directory containing the folder
    with the data files.  Defaults to "{data_dir}/states/".

    :type states_dir: str

    :returns: JSON -- The spectral data for this observation ID.

    Error codes:
    From parse_obsid_states:
    0 = No error parsing observation ID.
    1 = STATES spectral file not found.
    From this module:
    2 = Could not open one or more STATES file for reading.
    3 = STATES file did not have 4 columns to read.
    """

    # This error code will be used unless there's a problem reading any
    # of the STATES files in the list.
    errcode = 0

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y', 'xerr', 'yerr'])

    # For STATES, this defines the x-axis and y-axis units as a string.
    states_xunit = "microns"
    states_yunit = "(R_p/R_s)^2"

    # Parse the obsID string to determine the paths+files to read.
    parsed_files_result = parse_obsid_states(obsid, states_dir)
    errcode = parsed_files_result.errcode

    # For each file, read in the contents and create a return JSON object.
    if errcode == 0:
        for sfile in parsed_files_result.specfiles:
            try:
                wls, dwls, rprss, rprserrs = numpy.genfromtxt(sfile, unpack=True,
                                                              dtype=str,
                                                              comments='#')
                wls = [float(x) for x in wls]
                fls = [float(x) for x in rprss]
                xerr = [float(x) for x in dwls]
                yerr = [float(x) for x in rprserrs]
            except IOError:
                errcode = 2
                return_dataseries = DataSeries(
                    'states', obsid, [], [''], [''], [''], errcode)
            except ValueError:
                errcode = 3
                return_dataseries = DataSeries(
                    'states', obsid, [], [''], [''], [''], errcode)
            else:
                wlfls = [x for x in zip(wls, fls, xerr, yerr)]
                return_dataseries = DataSeries(
                    'states', obsid,
                    [[data_point(x=x, y=y, xerr=xerr, yerr=yerr) for
                      x, y, xerr, yerr in wlfls]],
                    ['STATES_' + obsid],
                    [states_xunit], [states_yunit], errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries(
            'states', obsid, [], [], [], [], errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
