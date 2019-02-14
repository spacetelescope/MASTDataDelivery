"""
.. module:: get_data_galex

   :synopsis: Returns extracted GALEX spectral data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
from astropy.io import fits
from .data_series import DataSeries
from .parse_obsid_galex import parse_obsid_galex

#--------------------
def get_data_galex(obsid, filt, url, missions_dir):
    """
    Given a GALEX observation ID, returns the spectral data.  Note that, in the
    case of GALEX, the obsID is not sufficient to locate the FITS file to read.
    Instead, in addition to the obsID a URL to the preview jpg the Portal uses
    is provided, which can be parsed to locate the FITS file to read.

    :param obsid: The GALEX observation ID to retrieve the data from.

    :type obsid: str

    :param filt: The filter for this GALEX observation ID.

    :type filt: str

    :param url: The URL for the preview jpg file for this obsID.

    :type url: str

    :param missions_dir: The path to the directory containing the "missions/"
    folder with the data files.

    :type missions_dir: str

    :returns: JSON -- The spectral data for this observation ID.

    Error codes:
    From parse_obsid_galex:
    0 = No error parsing observation ID.
    1 = Observation ID is a 2D spectral image, and not a 1D extracted spectrum.
    2 = Extracted spectra FITS file not found.
    From this module:
    3 = Could not open one or more FITS file for reading.
    4 = Filter value is not an accepted value.
    """

    # This error code will be used unless there's a problem reading any
    # of the FITS files in the list, or the spectrum is actually a 2D spectral
    # image.
    errcode = 0

    # This is for backwards compatability for the client version that did not
    # pass URL is a parameter.  Remove after client code is updated across
    # all versions.
    if url == "":
        errcode = 44

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For GALEX, this defines the x-axis and y-axis units as a string.
    galex_xunit = "Angstroms"
    galex_yunit = "ergs/cm^2/s/Angstrom"

    # Parse the obsID string to determine the paths+files to read.
    if filt.upper() in ["FUV", "NUV"] and errcode == 0:
        parsed_files_result = parse_obsid_galex(obsid, url, missions_dir)
        errcode = parsed_files_result.errcode
    elif errcode == 0:
        errcode = 4

    # For each file, read in the contents and create a return JSON object.
    # Note: Reference for *gsp.fits.gz FITS format is here:
    # http://www.galex.caltech.edu/researcher/files/gsp_columns_long.txt
    if errcode == 0:
        for sfile in parsed_files_result.specfiles:
            try:
                with fits.open(sfile) as hdulist:
                    wls = [float(x) for x in hdulist[1].data['wave'][0, :]]
                    fls = [float(x) for x in hdulist[1].data["flux"][0, :]]
            except IOError:
                errcode = 3
                return_dataseries = DataSeries(
                    'galex', obsid, [], [''], [''], [''], errcode)
            else:
                wlfls = [x for x in zip(wls, fls)]
                return_dataseries = DataSeries(
                    'galex', obsid,
                    [[data_point(x=x, y=y) for x, y in wlfls]],
                    ['GALEX_' + obsid + ' BAND:' + filt],
                    [galex_xunit], [galex_yunit], errcode)
    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries(
            'galex', obsid, [], [], [], [], errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
