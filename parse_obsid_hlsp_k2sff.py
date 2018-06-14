"""
.. module:: parse_obsid_hlsp_k2sff

   :synopsis: Given a K2SFF obsID returns the corresponding K2 target ID,
              file name, cadence type, campaign, etc.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import os
import re

#--------------------
def parse_obsid_hlsp_k2sff(obsid):
    """
    Given a K2SFF observation ID, returns the file to read.

    :param obsid: The K2SFF observation ID to retrieve the data from.

    :type obsid: str

    :returns: tuple -- An error code and a list of the set of files to read
    (including paths).

    Error codes:
    0 = No error parsing observation ID.
    1 = Error parsing K2SFF observation ID.
    2 = Cadence not recognized as long cadence.
    3 = File is missing on disk.
    """

    # Create namedtuple as the return object.
    parsed_values = collections.namedtuple('ParseResult', ['k2sffid',
                                                           'cadence',
                                                           'campaign',
                                                           'errcode', 'files'])

    # Initialize error code to 0 = pass.
    error_code = 0

    # Split the observation ID into K2SFF star name, campaign, and cadence.
    try:
        k2sffid, campaign, cadence = [
            x for x in re.split('k2sff|_|-', obsid) if x != '']
    except ValueError:
        error_code = 1
        return parsed_values(k2sffid='', cadence='', campaign='',
                             errcode=error_code, files=[''])

    # Make sure the cadence type is 'lc'.
    if cadence != 'lc':
        error_code = 2
        return parsed_values(k2sffid=k2sffid, cadence=cadence,
                             campaign=campaign, errcode=error_code, files=[''])

    # Use the observation ID to get paths to each file.
    dir_root = (os.path.pardir + os.path.sep + os.path.pardir + os.path.sep +
                "hlsps" + os.path.sep + "k2sff" +
                os.path.sep + campaign + os.path.sep)
    star_dir_root = (k2sffid[0:4] + "00000" + os.path.sep + k2sffid[4:] +
                     os.path.sep)

    # Generate FITS file name based on observation ID.
    file_name = ("hlsp_k2sff_k2_lightcurve_"+ k2sffid +
                 "-" + campaign + "_kepler_v1_llc.fits")
    full_file_name = dir_root + star_dir_root + file_name

    if os.path.isfile(full_file_name):
        return parsed_values(k2sffid=k2sffid, cadence=cadence,
                             campaign=campaign, errcode=error_code,
                             files=[full_file_name])
    error_code = 3
    return parsed_values(k2sffid=k2sffid, cadence=cadence,
                         campaign=campaign, errcode=error_code,
                         files=[full_file_name])
    #--------------------
