"""
.. module:: parse_obsid_galex

   :synopsis: Given a GALEX preview URL returns the corresponding FITS file
   name.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import os

#--------------------
def parse_obsid_galex(obsid, url):
    """
    Given an GALEX preview URL, return the FITS file to read.

    :param obsid: The GALEX observation ID to retrieve the data from.

    :type obsid: str

    :param url: The URL for the preview jpg file.

    :type url: str

    :returns: tuple -- An error code and a file to read, including the path.

    Error codes:
    0 = No error parsing observation ID.
    1 = Observation ID is a 2D spectral image, and not a 1D extracted spectrum.
    2 = Extracted spectra FITS file not found.
    """

    # Create namedtuple as the return object.
    parsed_values = collections.namedtuple('ParseResult', ['errcode',
                                                           'specfiles'])

    # Initialize error code to 0 = pass.
    error_code = 0

    # Check if this is a 2D spectral image.  The signpost is the presence of
    # an extension "int_2color.jpg".
    if url[-14:] == "int_2color.jpg":
        error_code = 1
        return parsed_values(errcode=error_code, specfiles=[''])

    # Generate the full path and name of the file to read.
    file_location = (os.path.pardir + os.path.sep + os.path.pardir +
                     os.path.sep + "missions" + os.path.sep + "galex" +
                     os.path.sep +
                     os.path.sep.join(url.split(os.path.sep)[2:-3]) +
                     os.path.sep + 'SSAP' + os.path.sep)

    # The name of the FITS file is equal to the GALEX observation ID.
    spec_file = file_location + obsid + ".fits"

    if os.path.isfile(spec_file):
        return parsed_values(errcode=error_code, specfiles=[spec_file])
    else:
        error_code = 2
        return parsed_values(errcode=error_code, specfiles=[''])
#--------------------
