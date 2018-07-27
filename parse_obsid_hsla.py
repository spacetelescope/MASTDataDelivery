"""
.. module:: parse_obsid_hsla

   :synopsis: Given an HSLA observation ID returns the corresponding FITS file
   name.  If a coadd-level spectrum, must also supply a target name.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
from glob import glob
import os
import numpy

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
                     'datapile_05-15-2018_COS' + os.path.sep + targ +
                     os.path.sep)

    # Check if directory exists.
    if not os.path.isdir(file_location):
        error_code = 1
        return parsed_values(errcode=error_code, specfiles=[''])

    # Look for FITS files.  If given an obsID of "hsla_coadd" then we look
    # for the "coadd" FITS files, otherwise we look for the Obs ID target.
    if obsid.lower().strip() == "hsla_coadd":
        pri_dataseries_patterns = ["FUVM_final_lpALL", "NUVM_final_lp1",
                                   "G140L_final_lpALL", "G230L_final_lp1"]
        # This list is the return set of files to be populated below.
        spec_files = []
        # Get all the available coadd files.
        all_spec_files = numpy.asarray(glob(file_location + "*coadd*.fits.gz"))
        # Make sure the list is sorted (for unit testing purposes).
        all_spec_files.sort()
        # Primary DataSeries are always returned, Secondary DataSeries
        # are returned if size limits allow.
        where_pri_spec_files = []
        where_sec_spec_files = []
        # Look for the primary DataSeries.
        for iindex, asf in enumerate(all_spec_files):
            is_pdb = False
            for pdp in pri_dataseries_patterns:
                if pdp in os.path.basename(asf):
                    # As soon as one primary data series string is found, add it
                    # to the list and don't need to check other primary data
                    # series strings.
                    where_pri_spec_files.append(iindex)
                    is_pdb = True
                    break
            if not is_pdb:
                where_sec_spec_files.append(iindex)
        # Add Primary Data Series to return object, if any were found.
        if where_pri_spec_files:
            spec_files.extend(all_spec_files[where_pri_spec_files])
        # Add remaining Secondary Data Series to the return object.
        if where_sec_spec_files:
            spec_files.extend(all_spec_files[where_sec_spec_files])
        if spec_files:
            return parsed_values(errcode=error_code, specfiles=spec_files)
        error_code = 2
        return parsed_values(errcode=error_code, specfiles=[''])
    exposure_level_file = file_location + obsid + "_x1d.fits"
    if os.path.isfile(exposure_level_file):
        return parsed_values(errcode=error_code,
                             specfiles=[exposure_level_file])
    error_code = 2
    return parsed_values(errcode=error_code, specfiles=[''])
#--------------------
