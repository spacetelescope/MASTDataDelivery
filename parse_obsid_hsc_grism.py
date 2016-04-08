"""
.. module:: parse_obsid_hsc_grism

   :synopsis: Given an HSC observation ID returns the corresponding FITS file
   name.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import os

#--------------------
def parse_obsid_hsc_grism(obsid):
    """
    Given an HSC grism observation ID, return the FITS file to read.

    :param obsid: The HSC grism observation ID to retrieve the data from.

    :type obsid: str

    :returns: tuple -- An error code and a file to read, including the path.

    Error codes:
    0 = No error parsing observation ID.
    1 = Observation ID is a 2D spectral image, and not a 1D extracted spectrum.
    2 = Error parsing observation ID to determine path of file on disk.
    3 = Extracted spectra FITS file not found.
    """

    # Create namedtuple as the return object.
    parsed_values = collections.namedtuple('ParseResult', ['errcode',
                                                           'specfiles'])

    # Initialize error code to 0 = pass.
    error_code = 0

    # Check if this is a 2D spectral image.  The signpost is the presence of
    # an extension ".spec2d.fits".
    if obsid[-12:] == ".spec2d.fits":
        error_code = 1
        return parsed_values(errcode=error_code, specfiles=[''])

    # Example ObservationID:
    # HAG_J033148.83-274850.4_UDFNICP2_V01.SPEC1D.FITS

    # Parse the observation ID to get components needed to get path.
    obsid_splits = obsid.lower().split('_')

    # Instrument part of path.
    if obsid_splits[0] == 'hag':
        obsid_instpart = 'acsgrism'
    elif obsid_splits[0] == 'hng':
        obsid_instpart = 'nicgrism'
    else:
        error_code = 2
        return parsed_values(errcode=error_code, specfiles=[''])
    # Subdirectory part of path.
    obsid_subdirpart = obsid_splits[2][0:4] + os.path.sep + obsid_splits[2][0:6]

    # Generate the full path and name of the file to read.
    file_location = (os.path.pardir + os.path.sep + os.path.pardir +
                     os.path.sep + "missions" + os.path.sep + "hst" +
                     os.path.sep + "hla" + os.path.sep + 'data24' +
                     os.path.sep + obsid_instpart + os.path.sep +
                     obsid_subdirpart + os.path.sep)

    # The name of the FITS file is the observation ID.
    spec_file = file_location + obsid.lower()

    if os.path.isfile(spec_file):
        return parsed_values(errcode=error_code, specfiles=[spec_file])
    else:
        error_code = 3
        return parsed_values(errcode=error_code, specfiles=[''])
#--------------------
