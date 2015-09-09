"""
.. module:: get_data_galex

   :synopsis: Returns extracted GALEX spectral data as a JSON string.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

from astropy.io import fits
import collections
from data_series import DataSeries
import numpy
import os
from parse_obsid_galex import parse_obsid_galex

#--------------------
def get_data_galex(obsid, filt, url):
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

    :returns: JSON -- The spectral data for this observation ID.

    Error codes:
    From parse_obsid_galex:
    0 = No error parsing observation ID.
    1 = Observation ID is a 2D spectral image, and not a 1D extracted spectrum.
    2 = Extracted spectra FITS file not found.
    3 = More than one spectral FITS file found.
    From this module:
    4 = Could not open one or more FITS file for reading.
    5 = Filter value is not an accepted value.
    6 = Target ID not found in flux table.
    """

    # This error code will be used unless there's a problem reading any
    # of the FITS files in the list, or the spectrum is actually a 2D spectral
    # image.
    errcode = 0

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For GALEX, this defines the x-axis and y-axis units as a string.
    galex_xunit = "Angstroms"
    galex_yunit = "photons/cm^2/s/Angstrom"

    # Parse the obsID string to determine the paths+files to read.
    if filt.upper() in ["FUV", "NUV"]:
        parsed_files_result = parse_obsid_galex(filt, url)
        errcode = parsed_files_result.errcode
    else:
        errcode = 5

    # For each file, read in the contents and create a return JSON object.
    # Note: Reference for *gsp.fits.gz FITS format is here:
    # http://www.galex.caltech.edu/researcher/files/gsp_columns_long.txt
    if errcode == 0:
        for sfile in parsed_files_result.specfiles:
            try:
                with fits.open(sfile) as hdulist:
                    # Get the extraction ID.
                    extract_ids = hdulist[1].data["id"]
                    # Get the total number of points per spectrum.
                    npts = hdulist[1].data["numpt"]
                    # Get the wavelength arrays.
                    wl_zeroes = hdulist[1].data["zero"]
                    wl_disp = hdulist[1].data["disp"]
                    # Since the Portal only has previews for coadds, we use
                    # the "OBJMDN" column for the spectral fluxes, which is only
                    # defined for visit-combined data.
                    fls_table = hdulist[1].data["objmdn"]

            except IOError:
                errcode = 4
                return_dataseries = DataSeries(
                    'galex', obsid, [], [''], [''], [''], errcode)
            else:
                # Locate this target in the 2D array.
                target_id = os.path.basename(url).split('id')[-1].split('-')[0]
                where_this_id = numpy.where(extract_ids == int(target_id))[0]
                if len(where_this_id) == 1:
                    # Construct the wavelengths.
                    ind = where_this_id[0]
                    wls = [float(wl_zeroes[ind]+(i*wl_disp[ind])) for i in
                           range(npts[ind])]
                    # Construct the fluxes.
                    fls = [float(fls_table[where_this_id[0], :][i]) for i in
                           range(npts[ind])]
                    wlfls = [x for x in zip(wls, fls)]
                    return_dataseries = DataSeries(
                        'galex', obsid,
                        [[data_point(x=x, y=y) for x, y in wlfls]],
                        ['GALEX_' + obsid + ' BAND:' + filt],
                        [galex_xunit], [galex_yunit], errcode)
                else:
                    errcode = 6
                    return_dataseries = DataSeries('galex', obsid, [], [''],
                                                   [''], [''], errcode)

    else:
        # This is where an error DataSeries object would be returned.
        return_dataseries = DataSeries(
            'galex', obsid, [], [], [], [], errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
