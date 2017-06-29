# Documentation on HLSP_K2EVEREST Lightcurve Data Returned by DataDelivery

## Description of HLSP_K2EVEREST Lightcurve Data Formats

HLSP_K2EVEREST are high level science products contributed by Rodrigo Luger (at the time, a graduate student at the Univ. of Washington).  The MAST HLSP page is located at https://archive.stsci.edu/prepds/everest/.  Not every K2 target has an EVEREST lightcurve.  The extracted, detrended lightcurves are stored in FITS files, one per K2 target.  Each target has both a **raw** and **corrected** version of the fluxes available, where the **corrected** fluxes have thruster firings and other systematics mitigated.

The FITS file has 5 extensions: the primary HDU with just a header, the data extension with the de-trended light curve, an extension with the coefficients for the linear model, an extension with the design matrix used in the linear model, and an image extension with the aperture used. The data extension (first extension) consists of the following columns:

* TIME - the time array (identical to input array from the K2 TPFs)
* FLUX - the de-trended flux array, in e-/s
* OUTLIER - an outlier mask. 0 if data point was used in the de-trending, 1 if it was masked as an outlier
* BKG_FLUX - the background flux we computed for campaigns 0,1, and 2. For the other campaigns this is zero, since the background is already pre-subtracted in the TPFs
* RAW_FLUX - the raw SAP flux in the aperture we used
* RAW_FERR - the raw SAP flux error

## Description of How DataDelivery Locates Data

DataDelivery only requires an observation ID to uniquely identify the FITS file to read from disk.  The HLSP_K2EVEREST observation IDs are stored in a subdirectory path that has the following format:

    subdir_path = c<##>/<####00000>/<#####>/

In the above formula, the first part is the 2-digit campaign number, the second part is the first four digits of the EPIC (target) ID, and the last part is the final five digits of the EPIC ID.  As an example, the observation ID "k2everest202059070-c00_lc" would lie in a subdirectory path of:

    v?/c00/202000000/59070/

The "v?" is the version number, e.g., "v1" or "v2".  The names of the FITS files are given by the following formula:

    "hlsp_everest_k2_llc_" + TRUNC_OBS_ID + "_kepler_v2.0_lc.fits"

In the above formula, TRUNC_OBS_ID is the observation ID *without* the "k2everest" or "_lc" substrings, e.g., "202059070-c00" for the observation ID "k2everest202059070-c00_lc".  For short cadence targets, the files end with "sc.fits" instead of "lc.fits".

## Description of Data Processing

Once the FITS file is located on disk, the time stamps, raw fluxes, and corrected fluxes are read.  The time stamps are stored in a truncated BJD format, where the full barycentric Julian date is given by:

    BJD[i] = BJDREFI + BJDREFF + TIME[i]

In the above formula, "BJDREFI" and "BJDREFF" are the integer and decimal components of the reference BJD date for the truncated time stamps.  These are located as header card values in the first FITS extension.  "TIME" is the array of truncated BJD time stamps, stored as a column in the first FITS extension.

Similarly, the **raw** and **corrected** fluxes are stored as columns in the data table of the first FITS extension, named "RAW_FLUX" and "FLUX", respectively.  No additional processing is performed on the fluxes, and no filtering based on quality flags or other selection criteria is performed.
