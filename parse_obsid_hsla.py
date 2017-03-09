"""
.. module:: parse_obsid_hsla

   :synopsis: Given an HSLA observation ID returns the corresponding FITS file
   name.  If a coadd-level spectrum, must also supply a target name.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
from glob import glob
import os

#--------------------
def parse_obsid_hsla(obsid, targ):
    """
    Given an HSLA grism observation ID, return the FITS file to read.  If a
    coadd-level spectrum, must also supply a target name.

    :param obsid: The HSLA grism observation ID to retrieve the data from.
    If a coadd-level spectrum, this should be set to "hsla_coadd" and it will
    be ignored.

    :type obsid: str

    :param targ: The target name, required if a coadd-level spectrum.

    :type targ: str

    :returns: tuple -- An error code and a file to read, including the path.

    Error codes:
    0 = No error parsing observation ID.
    1 = Directory not found.
    2 = Extracted spectra FITS file not found.
    """

    # Create namedtuple as the return object.
    parsed_values = collections.namedtuple('ParseResult', ['errcode',
                                                           'specfiles'])

    # Initialize error code to 0 = pass.
    error_code = 0

    # Example ObservationID:
    # lbgu22z3q
    # Example Target Name:
    # NGC-5548

    # Generate the full path and name of the file to read.
    file_location = (os.path.pardir + os.path.sep + os.path.pardir +
                     os.path.sep + "missions" + os.path.sep + "hst" +
                     os.path.sep + "spectral_legacy" + os.path.sep +
                     'datapile' + os.path.sep + targ + os.path.sep)

    # Check if directory exists.
    if not os.path.isdir(file_location):
        error_code = 1
        return parsed_values(errcode=error_code, specfiles=[''])

    # Look for FITS files.  If given an obsID of "hsla_coadd" then we look
    # for the "coadd" FITS files, otherwise we look for the Obs ID target.
    if obsid.lower().strip() == "hsla_coadd":
        spec_files = glob(file_location + "*coadd*.fits.gz")
        # Sort them for reproducibility and unit testing purposes.
        spec_files.sort()
        if len(spec_files) > 0:
            return parsed_values(errcode=error_code, specfiles=spec_files)
        else:
            error_code = 2
            return parsed_values(errcode=error_code, specfiles=[''])
    else:
        exposure_level_file = file_location + obsid + "_x1d.fits.gz"
        if os.path.isfile(exposure_level_file):
            return parsed_values(errcode=error_code,
                                 specfiles=[exposure_level_file])
        else:
            error_code = 2
            return parsed_values(errcode=error_code, specfiles=[''])
#--------------------
