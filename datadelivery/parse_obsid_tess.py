"""
.. module:: parse_obsid_tess

   :synopsis: Given a TESS obsID returns the corresponding TESS target ID,
              file name, Sector, etc.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import os
import re

#--------------------
def parse_obsid_tess(obsid, missions_dir):
    """
    Given a TESS observation ID, returns the file to read.

    :param obsid: The TESS observation ID to retrieve the data from.

    :type obsid: str

    :param missions_dir: The path to the directory containing the "missions/"
    folder with the data files.

    :type missions_dir: str

    :returns: tuple -- An error code and a list of the set of files to read
    (including paths).

    Error codes:
    0 = No error parsing observation ID.
    1 = Error parsing TESS observation ID.
    2 = File is missing on disk.
    3 = Target pixel file only.
    """

    # Create namedtuple as the return object.
    parsed_values = collections.namedtuple('ParseResult', ['tessid',
                                                           'sector',
                                                           'errcode', 'files'])

    # Initialize error code to 0 = pass.
    error_code = 0

    # Split the observation ID into TESS star name and Sector.
    try:
        _, sector, tessid, _, _ = [
            x for x in re.split('_|-', obsid) if x != '']
    except ValueError:
        error_code = 1
        return parsed_values(tessid='', sector='',
                             errcode=error_code, files=[''])

    # Use the observation ID to get paths to each file.
    dir_root = (missions_dir + os.path.sep + "tess" + os.path.sep + 'tid' +
                os.path.sep + sector + os.path.sep)
    star_dir_root = (tessid[0:4] + os.path.sep + tessid[4:8] +os.path.sep +
                     tessid[8:12] + os.path.sep + tessid[12:16] + os.path.sep)

    file_name = (obsid + "_lc.fits")
    tp_file_name = (obsid + "_tp.fits")
    full_file_name = dir_root + star_dir_root + file_name
    tp_full_file_name = dir_root + star_dir_root + tp_file_name

    if os.path.isfile(full_file_name):
        return parsed_values(tessid=tessid,
                             sector=sector, errcode=error_code,
                             files=[full_file_name])
    elif os.path.isfile(tp_full_file_name):
        error_code = 3
        return parsed_values(tessid=tessid,
                             sector=sector, errcode=error_code,
                             files=[tp_full_file_name])
    error_code = 2
    return parsed_values(tessid=tessid,
                         sector=sector, errcode=error_code,
                         files=[full_file_name])
#--------------------
