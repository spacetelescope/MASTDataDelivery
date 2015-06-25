"""
.. module:: parse_obsid_kepler

   :synopsis: Given a Kepler obsID returns the corresponding Kepler ID,
              Quarters, file names, cadence type, etc.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import os
import re

#--------------------
# Define the look-up tables between Quarter number and epoch string(s).
LONG_QUARTER_PREFIXES = {'0':['2009131105131'],
                         '1':['2009166043257'],
                         '2':['2009259160929'],
                         '3':['2009350155506'],
                         '4':['2010078095331', '2010009091648'],
                         '5':['2010174085026'],
                         '6':['2010265121752'],
                         '7':['2010355172524'],
                         '8':['2011073133259'],
                         '9':['2011177032512'],
                         '10':['2011271113734'],
                         '11':['2012004120508'],
                         '12':['2012088054726'],
                         '13':['2012179063303'],
                         '14':['2012277125453'],
                         '15':['2013011073258'],
                         '16':['2013098041711'],
                         '17':['2013131215648']}

SHORT_QUARTER_PREFIXES = {'0':['2009131110544'],
                          '1':['2009166044711'],
                          '2':['2009201121230', '2009231120729',
                               '2009259162342'],
                          '3':['2009291181958', '2009322144938',
                               '2009350160919'],
                          '4':['2010009094841', '2010019161129',
                               '2010049094358', '2010078100744'],
                          '5':['2010111051353', '2010140023957',
                               '2010174090439'],
                          '6':['2010203174610', '2010234115140',
                               '2010265121752'],
                          '7':['2010296114515', '2010326094124',
                               '2010355172524'],
                          '8':['2011024051157', '2011053090032',
                               '2011073133259'],
                          '9':['2011116030358', '2011145075126',
                               '2011177032512'],
                          '10':['2011208035123', '2011240104155',
                                '2011271113734'],
                          '11':['2011303113607', '2011334093404',
                                '2012004120508'],
                          '12':['2012032013838', '2012060035710',
                                '2012088054726'],
                          '13':['2012121044856', '2012151031540',
                                '2012179063303'],
                          '14':['2012211050319', '2012242122129',
                                '2012277125453'],
                          '15':['2012310112549', '2012341132017',
                                '2013011073258'],
                          '16':['2013017113907', '2013065031647',
                                '2013098041711'],
                          '17':['2013121191144', '2013131215648']}

QUARTER_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
#--------------------

#--------------------
def parse_obsid_kepler(obsid):
    """
    Given a Kepler observation ID, returns the set of files to read.

    :param obsid: The Kepler observation ID to retrieve the data from.

    :type obsid: str

    :returns: tuple -- An error code and a list of the set of files to read
    (including paths).

    Error codes:
    0 = No error parsing observation ID.
    1 = Could not unpack observation ID into three components.
    2 = Kepler ID in Observation ID string not within allowed bounds.
    3 = Kepler cadence type in Observation ID not an allowed value.
    4 = Kepler Q-code in Observation ID is not exactly 18 characters.
    5 = One or more files are missiong on disk based on the Q-code.
    """

    # Create namedtuple as the return object.
    parsed_values = collections.namedtuple('ParseResult', ['kepid', 'cadence',
                                                           'errcode',
                                                           'quarters', 'files'])

    # Initialize error code to 0 = pass.
    error_code = 0

    # Split the observation ID into Kepler star name, cadence, and Q code.
    try:
        kepid, cadence, qcode = [x for x in re.split('_|kplr|q', obsid) if
                                 x != '']
    except ValueError:
        error_code = 1
        return parsed_values(kepid='', cadence='', errcode=error_code,
                             files=[''], quarters=[''])

    # Make sure the Kepler ID is within allowed bounds.
    if int(kepid) < 757076 or int(kepid) > 100004300:
        error_code = 2
        return parsed_values(kepid=kepid, cadence=cadence, errcode=error_code,
                             files=[''], quarters=[''])

    # Make sure the cadence type is either 'lc' or 'sc'.
    if cadence != 'sc' and cadence != 'lc':
        error_code = 3
        return parsed_values(kepid=kepid, cadence=cadence, errcode=error_code,
                             files=[''], quarters=[''])

    # Make sure the Q code is exactly 18 characters.
    if len(qcode) != 18:
        error_code = 4
        return parsed_values(kepid=kepid, cadence=cadence, errcode=error_code,
                             files=[''], quarters=[''])

    # Use the Q code to get paths to each file.
    all_files = []
    all_quarters = []
    dir_root = (os.path.pardir + os.path.sep + os.path.pardir + os.path.sep +
                "missions" + os.path.sep + "kepler" + os.path.sep +
                "lightcurves" + os.path.sep)
    star_dir_root = kepid[0:4] + os.path.sep + kepid + os.path.sep

    # Populate long cadence files if the cadence type is LC.
    if cadence == 'lc':
        for i, q_c in enumerate(qcode):
            files_to_add = [
                dir_root + star_dir_root + 'kplr' + kepid + '-' + x +
                '_llc.fits' for x in LONG_QUARTER_PREFIXES[str(i)] if
                os.path.isfile(
                    dir_root + star_dir_root + 'kplr'
                    + kepid + '-' + x + '_llc.fits')]
            if len(files_to_add) == int(q_c):
                all_files.extend(files_to_add)
                all_quarters.extend([str('{0:02d}'.format(i))] *
                                    len(files_to_add))
            else:
                error_code = 5
                return parsed_values(kepid=kepid, cadence=cadence,
                                     errcode=error_code, files=[''],
                                     quarters=[''])

    # Populate long cadence files if the cadence type is SC.
    if cadence == 'sc':
        for i, q_c in enumerate(qcode):
            files_to_add = [
                dir_root + star_dir_root + 'kplr' + kepid + '-' + x +
                '_slc.fits' for x in SHORT_QUARTER_PREFIXES[str(i)] if
                os.path.isfile(
                    dir_root + star_dir_root + 'kplr'
                    + kepid + '-' + x + '_slc.fits')]
            if len(files_to_add) == int(q_c):
                all_files.extend(files_to_add)
                all_quarters.extend([''.join(x) for x in
                                     zip([str('{0:02d}'.format(i))] *
                                         len(files_to_add), QUARTER_LETTERS)])
            else:
                error_code = 5
                return parsed_values(kepid=kepid, cadence=cadence,
                                     errcode=error_code, files=[''],
                                     quarters=[''])

    # Return the list of files.
    return parsed_values(kepid=kepid, cadence=cadence, errcode=error_code,
                         files=all_files, quarters=all_quarters)
#--------------------
