# Documentation on HLSP_K2SFF Lightcurve Data Returned by DataDelivery

## Description of HLSP_K2SFF Lightcurve Data Formats

HLSP_K2SFF are high level science products contributed by Andrew Vanderburg (at the time, a graduate student at Harvard).  The MAST HLSP page is located at https://archive.stsci.edu/prepds/k2sff/.  Not every K2 target has a K2SFF lightcurve, for example, short cadence targets are not included in K2SFF.  The extracted, detrended lightcurves are stored in FITS files, one per K2 target.  For each target, there are **twenty** different fluxes available, each one using a different sized/shaped photometric aperture.  Furthermore, each of those twenty apertures have both a **raw** and **corrected** version of the fluxes available, where the **corrected** fluxes have thruster firings and other systematics mitigated.

The first FITS extension contains a data table that has the time stamps and fluxes for the photometric aperture that their software concluded was "the best" aperture choice.  This is an automated decision, however, so all twenty apertures, including the one that the software decided was "best", are included in FITS extensions #2-21.  Their data formats are all the same:  data tables containing time stamps, fluxes, and other metadata.  The 22nd and 23rd FITS extensions contain data tables that define each of the circular and PSF apertures, respectively (e.g., the sizes of the first and second set of ten apertures, respectively).  The 24th extension contains the summed image of all the postage stamp frames.  Only extensions #1-21 contain the data series themselves, so those are the one's most important to DataDelivery.

## Description of How DataDelivery Locates Data

DataDelivery only requires an observation ID to uniquely identify the FITS file to read from disk.  The HLSP_K2SFF observation IDs are stored in a subdirectory path that has the following format:

    subdir_path = c<##>/<####00000>/<#####>/

In the above formula, the first part is the 2-digit campaign number, the second part is the first four digits of the EPIC (target) ID, and the last part is the final five digits of the EPIC ID.  As an example, the observation ID "k2sff202059070-c00_lc" would lie in a subdirectory path of:

    c00/202000000/59070/

The names of the FITS files are given by the following formula:

    "hlsp_k2sff_k2_lightcurve_" + TRUNC_OBS_ID + "_kepler_v1_llc.fits"

In the above formula, TRUNC_OBS_ID is the observation ID *without* the "k2sff" or "_lc" substrings, e.g., "202059070-c00" for the observation ID "k2sff202059070-c00_lc".  If there are ever any short cadence targets provided as part of HLSP_K2SFF, the files will end with "slc.fits" instead of "llc.fits".

## Description of Data Processing

Once the FITS file is located on disk, the time stamps, raw fluxes, and corrected fluxes for each of the fluxes in FITS extensions #1-21 are read.  A reminder that the first extension is a copy of one of the other twenty aperture results that has been determined as the "best" choice by the software.  Since it is convenient to have access to this series, it is included along with all the twenty apertures with its own label.  The time stamps are stored in a truncated BJD format, where the full barycentric Julian date is given by:

    BJD[i] = BJDREFI + BJDREFF + T[i]

In the above formula, "BJDREFI" and "BJDREFF" are the integer and decimal components of the reference BJD date for the truncated time stamps.  These are located as header card values in the given aperture's FITS extension.  "T" is the array of truncated BJD time stamps, stored as a column in that aperture's data table in its FITS extension.

Similarly, the **raw** and **corrected** fluxes are stored as columns in the data table for the given aperture's FITS extension, named "FRAW" and "FCOR", respectively.  No additional processing is performed on the fluxes, and no filtering based on quality flags or other selection criteria is performed.
