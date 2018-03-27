"""
.. module:: parse_obsid_iue

   :synopsis: Given an IUE obsID returns the corresponding file name.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import os

#--------------------
def parse_obsid_iue(obsid, filt):
    """
    Given an IUE observation ID, return the file to read.

    :param obsid: The IUE observation ID to retrieve the data from.

    :type obsid: str

    :param filt: The filter for this IUE observation ID.  It must be either
    "LOW_DISP" or "HIGH_DISP".

    :type filt: str

    :returns: tuple -- An error code and a file to read, including the path.

    Error codes:
    0 = No error parsing observation ID.
    1 = Observation ID does not begin with expected first three letters.
    2 = No mxlo or mxhi file found on disk.
    """

    # Create namedtuple as the return object.
    parsed_values = collections.namedtuple('ParseResult', ['errcode',
                                                           'specfiles'])

    # Initialize error code to 0 = pass.
    error_code = 0

    # Make sure the first three letters are from the expected set of choices.
    if obsid[0:3] not in ["lwp", "lwr", "swp"]:
        error_code = 1
        return parsed_values(errcode=error_code, specfiles=[''])

    # Generate the full path and name of the file to read.
    file_location = (os.path.pardir + os.path.sep + os.path.pardir +
                     os.path.sep + "missions" + os.path.sep + "iue" +
                     os.path.sep + "data" + os.path.sep + obsid[0:3] +
                     os.path.sep + obsid[3:5] + "000" + os.path.sep)

    # The file we want is either a *mxlo* or a *mxhi* FITS file (compressed).
    mxlo_file = file_location + obsid + ".mxlo.gz"
    mxhi_file = file_location + obsid + ".mxhi.gz"

    # Identify which file to return based on the FILTER requested.
    if filt == "LOW_DISP":
        file_to_return = mxlo_file
    elif filt == "HIGH_DISP":
        file_to_return = mxhi_file
    elif filt == "UNKNOWN":
        if os.path.isfile(mxhi_file):
            file_to_return = mxhi_file
        else:
            file_to_return = mxlo_file

    if os.path.isfile(file_to_return):
        return parsed_values(errcode=error_code, specfiles=[file_to_return])
    error_code = 2
    return parsed_values(errcode=error_code, specfiles=[''])
#--------------------
