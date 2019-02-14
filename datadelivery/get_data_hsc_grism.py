"""
.. module:: get_data_hsc_grism

   :synopsis: Returns extracted ACS or NICMOS grism spectra from HLA. These
   come from being cross-matched with the Hubble Source Catalog (HSC).

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
from astropy.io import fits
from .data_series import DataSeries
from .parse_obsid_hsc_grism import parse_obsid_hsc_grism

#--------------------
def get_data_hsc_grism(obsid, missions_dir):
    """
    Given an HLA grism observation ID, returns the spectral data.

    :param obsid: The HLA grism observation ID to retrieve the data from.

    :type obsid: str

    :param missions_dir: The path to the directory containing the "missions/"
    folder with the data files.

    :type missions_dir: str

    :returns: JSON -- The spectral data for this observation ID.

    Error codes:
    From parse_obsid_hsc_grism:
    0 = No error parsing observation ID.
    1 = Observation ID is a 2D spectral image, and not a 1D extracted spectrum.
    2 = Error parsing observation ID to determine path of file on disk.
    3 = Extracted spectra FITS file not found.
    From this module:
    4 = Could not open one or more FITS file for reading.
    """

    # This error code will be used unless there's a problem reading any
    # of the FITS files in the list, or the spectrum is actually a 2D spectral
    # image.
    errcode = 0

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For HLA grisms, this defines the x-axis and y-axis units as a string.
    hsc_grism_xunit = "Angstroms"
    hsc_grism_yunit = "ergs/cm^2/s/Angstrom"

    # Parse the obsID string to determine the paths+files to read.
    parsed_files_result = parse_obsid_hsc_grism(obsid, missions_dir)
    errcode = parsed_files_result.errcode

    # For each file, read in the contents and create a return JSON object.
    if errcode == 0:
        for sfile in parsed_files_result.specfiles:
            try:
                with fits.open(sfile) as hdulist:
                    wls = [float(x) for x in hdulist[1].data['wave'][0, :]]
                    fls = [float(x) for x in hdulist[1].data["flux"][0, :]]
            except IOError:
                errcode = 4
                return_dataseries = DataSeries(
                    'hsc_grism', obsid, [], [''], [''], [''], errcode)
            else:
                wlfls = [x for x in zip(wls, fls)]
                return_dataseries = DataSeries(
                    'hsc_grism', obsid,
                    [[data_point(x=float("{0:.8e}".format(x)),
                                 y=float("{0:.8e}".format(y)))
                      for x, y in wlfls]],
                    [obsid],
                    [hsc_grism_xunit], [hsc_grism_yunit],
                    errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries(
            'hsc_grism', obsid, [], [], [], [], errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
