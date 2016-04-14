# Documentation on HLSP_K2SC Lightcurve Data Returned by DataDelivery

## Description of HLSP_K2SC Lightcurve Data Formats

HLSP_K2SC are high level science products contributed by Suzanne Aigrain.  The MAST HLSP page is located at https://archive.stsci.edu/prepds/k2sc/.  Not every K2 target has a K2SC lightcurve, for example, short cadence targets are not included in K2SC.  The extracted, detrended lightcurves are stored in FITS files, one per K2 target.  For each target, there are **two** different, detrended fluxes available.  The first FITS extension contains a data table that has the time stamps and fluxes for the detrended **PDCSAP** fluxes.  The second FITS extension contains a data table that has the time stamps and fluxes for the detrended **SAP** fluxes.

## Description of How DataDelivery Locates Data

DataDelivery only requires an observation ID to uniquely identify the FITS file to read from disk.  The HLSP_K2SC observation IDs are stored in a subdirectory path that has the following format:

    subdir_path = c<##>/<####00000>/

In the above formula, the first part is the 2-digit campaign number, and the second part is the first four digits of the EPIC (target) ID.  As an example, the observation ID "k2sc200004923-c03_lc" would lie in a subdirectory path of:

    c03/200000000/

The names of the FITS files are given by the following formula:

    "hlsp_k2sc_k2_llc_" + TRUNC_OBS_ID + "_kepler_v1_lc.fits"

In the above formula, TRUNC_OBS_ID is the observation ID *without* the "k2sc" or "_lc" substrings, e.g., "200004923-c03" for the observation ID "k2sc200004923-c03_lc".  If there are ever any short cadence targets provided as part of HLSP_K2SC, the files will end with "sc.fits" instead of "lc.fits".

## Description of Data Processing

Once the FITS file is located on disk, the time stamps and corrected fluxes for each of the FITS extensions #1 and 2 are read.  The time stamps are stored in a truncated BJD format, where the full barycentric Julian date is given by:

    BJD[i] = TIME[i] + 2454833.0

In the above formula, "TIME" is the array of truncated BJD time stamps, stored as a column in the data tables in each FITS extension.  Similarly, the detrended fluxes are stored as a column called "FLUX".  No additional processing is performed on the fluxes, and no filtering based on quality flags or other selection criteria is performed.

