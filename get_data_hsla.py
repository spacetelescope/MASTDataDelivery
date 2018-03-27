"""
.. module:: get_data_hsla

   :synopsis: Returns coadded or exposure-level spectra from the
              Hubble Spectroscopic Legacy Archive.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import collections
import os
from astropy.io import fits
from data_series import DataSeries
from parse_obsid_hsla import parse_obsid_hsla

#--------------------
def get_data_hsla(obsid, targ):
    """
    Given an HSLA observation ID, returns the spectral data.  If a
    coadd-level spectrum, must supply the target name via the 'targ'
    parameter.

    :param obsid: The HSLA grism observation ID to retrieve the data from.

    :type obsid: str

    :param targ: The name of the target, if a coadd-level spectrum.

    :type targ: str

    :returns: JSON -- The spectral data for this observation ID.

    Error codes:
    From parse_obsid_hsla_grism:
    0 = No error parsing observation ID.
    1 = Directory not found.
    2 = Extracted spectra FITS file not found.
    From this module:
    3 = Could not open one or more FITS file for reading.
    """

    # This error code will be used unless there's a problem reading any
    # of the FITS files in the list.
    errcode = 0

    # This defines a data point for a DataSeries object as a namedtuple.
    data_point = collections.namedtuple('DataPoint', ['x', 'y'])

    # For HSLA grisms, this defines the x-axis and y-axis units as a string.
    hsla_xunit = "Angstroms"
    hsla_yunit = "ergs/cm^2/s/Angstrom"

    # Parse the obsID string to determine the paths+files to read.
    parsed_files_result = parse_obsid_hsla(obsid, targ)
    errcode = parsed_files_result.errcode

    # We create a list of return DataSeries for each segment.
    all_data_series = []

    # For each file, read in the contents and create a return JSON object.
    if errcode == 0:
        for sfile in parsed_files_result.specfiles:
            try:
                with fits.open(sfile) as hdulist:
                    if obsid.lower().strip() != "hsla_coadd":
                        # Get the segments, which can be ['FUVA' or 'FUVB']
                        segments = hdulist[1].data['segment']
                        # Wavelengths and fluxes are stored as a list for
                        # each seg.
                        segment_wls = hdulist[1].data['wavelength']
                        segment_fls = hdulist[1].data["flux"]
                        segment_flerrs = hdulist[1].data["error"]
                    else:
                        # Then this is a coadd, so there aren't multiple segs.
                        wls = hdulist[1].data['wave']
                        fls = hdulist[1].data["fluxwgt"]
                        flerrs = hdulist[1].data["fluxwgt_err"]
            except IOError:
                errcode = 4
                all_data_series.append(DataSeries(
                    'hsla', obsid, [], [''], [''], [''], errcode,
                    is_ancillary=[1]))
            else:
                # Create DataSeries if this is an exposure-level spectrum.
                if obsid.lower().strip() != "hsla_coadd":
                    for this_seg, this_wl, this_fl, this_flerr in zip(
                            segments, segment_wls, segment_fls, segment_flerrs):
                        wls = [float(x) for x in this_wl]
                        fls = [float(x) for x in this_fl]
                        flerrs = [float(x) for x in this_flerr]
                        wlfls = [x for x in zip(wls, fls)]
                        wlfls_err = [x for x in zip(wls, flerrs)]
                        # Append the wl-fl DataSeries for this segment.
                        all_data_series.append(DataSeries(
                            'hsla', obsid,
                            [[data_point(x=float("{0:.8e}".format(x)),
                                         y=float("{0:.8e}".format(y)))
                              for x, y in wlfls]],
                            [obsid+'_'+this_seg], [hsla_xunit], [hsla_yunit],
                            errcode, is_ancillary=[0]))
                        # Append the wl-flerr DataSeries for this segment.
                        all_data_series.append(DataSeries(
                            'hsla', obsid,
                            [[data_point(x=float("{0:.8e}".format(x)),
                                         y=float("{0:.8e}".format(y)))
                              for x, y in wlfls_err]],
                            [obsid+'_'+this_seg+'_ERR'], [hsla_xunit],
                            [hsla_yunit], errcode, is_ancillary=[1]))
                else:
                    # Create DataSeries if this is a coadd-level spectrum.
                    wls = [float(x) for x in wls]
                    fls = [float(x) for x in fls]
                    flerrs = [float(x) for x in flerrs]
                    wlfls = [x for x in zip(wls, fls)]
                    wlfls_err = [x for x in zip(wls, flerrs)]
                    # Only plot the coadd across lifetime positions by default.
                    if '_all.fits.gz' in os.path.basename(sfile):
                        is_anc = [0]
                    else:
                        is_anc = [1]
                    # Append the wl-fl DataSeries for this segment.
                    all_data_series.append(DataSeries(
                        'hsla', obsid,
                        [[data_point(x=float("{0:.8e}".format(x)),
                                     y=float("{0:.8e}".format(y)))
                          for x, y in wlfls]],
                        [os.path.basename(sfile).strip(".fits.gz")],
                        [hsla_xunit], [hsla_yunit], errcode,
                        is_ancillary=is_anc))
                    # Append the wl-flerr DataSeries for this segment.
                    all_data_series.append(DataSeries(
                        'hsla', obsid,
                        [[data_point(x=float("{0:.8e}".format(x)),
                                     y=float("{0:.8e}".format(y)))
                          for x, y in wlfls_err]],
                        [os.path.basename(sfile).strip(".fits.gz")+'_ERR'],
                        [hsla_xunit], [hsla_yunit],
                        errcode, is_ancillary=[1]))
    else:
        # This is where an error DataSeries object would be returned.
        all_data_series.append(DataSeries(
            'hsla', obsid, [], [], [], [], errcode, is_ancillary=[1]))

    # Return the DataSeries object back to the calling module.
    if len(all_data_series) == 1:
        return all_data_series[0]
    return all_data_series
#--------------------
