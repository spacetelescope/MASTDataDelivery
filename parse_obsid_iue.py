"""
.. module:: parse_obsid_iue

   :synopsis: Given an IUE obsID returns the corresponding file name.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import os

#--------------------
def parse_obsid_iue(obsid):
    """
    Given an IUE observation ID, return the file to read.

    :param obsid: The IUE observation ID to retrieve the data from.

    :type obsid: str

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

    # Identify which file to return.  It should be one or both.
    if os.path.isfile(mxlo_file) or os.path.isfile(mxhi_file):
        return parsed_values(errcode=error_code, specfiles=[x for x in
                                                            [mxlo_file,
                                                             mxhi_file] if
                                                            os.path.isfile(x)])
    else:
        error_code = 2
        return parsed_values(errcode=error_code, specfiles=[''])
#--------------------
