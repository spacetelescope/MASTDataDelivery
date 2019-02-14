"""
.. module:: parse_obsid_k2

   :synopsis: Given a K2 obsID returns the corresponding K2 target ID,
              file name, cadence type, campaign, etc.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import os
import re

#--------------------
def parse_obsid_k2(obsid, missions_dir):
    """
    Given a K2 observation ID, returns the file to read.

    :param obsid: The K2 observation ID to retrieve the data from.

    :type obsid: str

    :param missions_dir: The path to the directory containing the "missions/"
    folder with the data files.

    :type missions_dir: str

    :returns: tuple -- An error code and a list of the set of files to read
    (including paths).

    Error codes:
    0 = No error parsing observation ID.
    1 = Error parsing K2 observation ID.
    2 = Cadence not recognized as long or short cadence.
    3 = File is missing on disk.
    """

    # Create namedtuple as the return object.
    parsed_values = collections.namedtuple('ParseResult', ['k2id',
                                                           'cadence',
                                                           'campaign',
                                                           'errcode', 'files'])

    # Initialize error code to 0 = pass.
    error_code = 0

    # Split the observation ID into K2 star name, campaign, and cadence.
    try:
        k2id, campaign, cadence = [
            x for x in re.split('ktwo|_|-', obsid) if x != '']
    except ValueError:
        error_code = 1
        return parsed_values(k2id='', cadence='', campaign='',
                             errcode=error_code, files=[''])

    # If Campaign 10, then the light curves live in the Campaign 10-2 subdir
    # (there are none from Campaign 10-1), so we have to translate the Campaign
    # number.
    if campaign == 'c10':
        campaign = 'c102'

    # The part of the directory with the campaign number is *not* zero-padded.
    campaign_subdir = 'c'+'{0:2d}'.format(int(campaign[1:])).strip()

    # Make sure the cadence type is 'lc' or 'sc'.
    if cadence not in ('lc', 'sc'):
        error_code = 2
        return parsed_values(k2id=k2id, cadence=cadence,
                             campaign=campaign, errcode=error_code, files=[''])

    # Use the observation ID to get paths to each file.
    dir_root = (missions_dir + os.path.sep + "k2" + os.path.sep + "lightcurves" +
                os.path.sep + campaign_subdir + os.path.sep)
    star_dir_root = (k2id[0:4] + "00000" + os.path.sep + k2id[4:6] + "000" +
                     os.path.sep)

    # Generate FITS file name based on observation ID.
    if cadence == 'lc':
        cadence_str = '_llc'
    elif cadence == 'sc':
        cadence_str = '_slc'
    file_name = ("ktwo"+ k2id +
                 "-" + campaign + cadence_str + ".fits")
    full_file_name = dir_root + star_dir_root + file_name

    if os.path.isfile(full_file_name):
        return parsed_values(k2id=k2id, cadence=cadence,
                             campaign=campaign, errcode=error_code,
                             files=[full_file_name])
    error_code = 3
    return parsed_values(k2id=k2id, cadence=cadence,
                         campaign=campaign, errcode=error_code,
                         files=[full_file_name])
    #--------------------
