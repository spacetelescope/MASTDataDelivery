# Documentation on HLSP_K2VARCAT Lightcurve Data Returned by DataDelivery

## Description of HLSP_K2VARCAT Lightcurve Data Formats

HLSP_K2VARCAT are high level science products contributed by David Armstrong (at the time, a research fellow at University of Warwick).  The MAST HLSP page is located at https://archive.stsci.edu/prepds/k2varcat/.  Not every K2 target has a K2VARCAT lightcurve: only those *long cadence* sources that the team found to be variable are included in K2VARCAT.  The extracted, detrended lightcurves are stored in FITS files, one per K2 target.  For each target, there are **two** different fluxes available:  an **extracted** and a **detrended**.  The first is extracted but not detrended, while the second was extracted and had thruster firings and other systematics mitigated.

The first FITS extension contains a data table that has the time stamps and fluxes.  The second extension contains the aperture mask used to extract the fluxes, but this is not used by DataDelivery.

## Description of How DataDelivery Locates Data

DataDelivery only requires an observation ID to uniquely identify the FITS file to read from disk.  The HLSP_K2VARCAT observation IDs are stored in a subdirectory path that has the following format:

    subdir_path = c<##>/<####00000>/<##000>/

In the above formula, the first part is the 2-digit campaign number, the second part is the first four digits of the EPIC (target) ID, and the last part is the 5th and 6th digits of the EPIC ID.  As an example, the observation ID "k2varcat202059697-c00_lc" would lie in a subdirectory path of:

    c00/202000000/59000/

The names of the FITS files are given by the following formula:

    "hlsp_k2varcat_k2_lightcurve_" + TRUNC_OBS_ID + "_kepler_v2_llc.fits"

In the above formula, TRUNC_OBS_ID is the observation ID *without* the "k2varcat" or "_lc" substrings, e.g., "202059697-c00" for the observation ID "k2varcat202059697-c00_lc".  If there are ever any short cadence targets provided as part of HLSP_K2VARCAT, the files will end with "slc.fits" instead of "llc.fits".

## Description of Data Processing

Once the FITS file is located on disk, the time stamps, extracted fluxes, and detrended fluxes are read.  The time stamps are stored in a truncated BJD format, where the full barycentric Julian date is given by:

    BJD[i] = BJD_REF + TIME[i]

In the above formula, "BJD_REF" is the truncated value to add to the time stamps.  This is extracted as a substring from the header card value "TUNIT1" in the first FITS extension.  "TIME" is the array of truncated BJD time stamps, stored as a column in the first extension's data table.

Similarly, the **extracted** and **detrended** fluxes are stored as columns in the data table in the first FITS extension, named "APTFLUX" and "DETFLUX", respectively.  No additional processing is performed on the fluxes, and no filtering based on quality flags or other selection criteria is performed.
