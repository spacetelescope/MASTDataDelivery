"""
.. module:: parse_obsid_states

   :synopsis: Given a STATES observation ID returns the corresponding STATES
              spectral file.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import os

#--------------------
def parse_obsid_states(obsid):
    """
    Given an STATES observation ID, return the spectral file to read.

    :param obsid: The STATES observation ID to retrieve the data from.

    :type obsid: str

    :returns: tuple -- An error code and a file to read, including the path.

    Error codes:
    0 = No error parsing observation ID.
    1 = Extracted spectral file not found.
    """

    # Create namedtuple as the return object.
    parsed_values = collections.namedtuple('ParseResult', ['errcode',
                                                           'specfiles'])

    # Initialize error code to 0 = pass.
    error_code = 0

    # Generate the full path and name of the file to read.
    file_location = (os.path.pardir + os.path.sep + os.path.pardir +
                     os.path.sep + "states" + os.path.sep +
                     "transmission_spectra" + os.path.sep)

    # The name of the file is equal to the STATES observation ID.
    spec_file = file_location + obsid + ".txt"

    if os.path.isfile(spec_file):
        return parsed_values(errcode=error_code, specfiles=[spec_file])
    error_code = 1
    return parsed_values(errcode=error_code, specfiles=[''])
#--------------------
