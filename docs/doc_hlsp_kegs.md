# Documentation on HLSP_KEGS Lightcurve Data Returned by DataDelivery

## Description of HLSP_KEGS Lightcurve Data Formats

HLSP_KEGS are high level science products contributed by Edward Shaya and team.  The MAST HLSP page is located at https://archive.stsci.edu/prepds/kegs/.  Not every K2 target has a KEGS lightcurve, for example, short cadence targets are not included in KEGS, and KEGS is a project that only includes extragalactic targets.  The team starts with the K2-mission-produced target pixel files and then creates their own detrended light curves, including their own cotrending basis vectors (CBVs).  They provide one file per target, which contains in the first FITS extension a binary table of five different detrended fluxes, as well as the raw (or non-detrended).

## Description of How DataDelivery Locates Data

DataDelivery only requires an observation ID to uniquely identify the KEGS file to read from disk.  The HLSP_KEGS observation IDs are stored in a subdirectory path that has the following format:

    subdir_path = c<##>/<####00000>/<#####>/

In the above formula, the first part is the 2-digit campaign number, the second part is the first four digits of the EPIC (target) ID, and the last part is the final five digits of the EPIC ID.  As an example, the observation ID "kegs220163813-c08_lc" would lie in a subdirectory path of:

    c08/220100000/63813/

The names of the light curve files are given by the following formula:

    "hlsp_kegs_k2_lightcurve_" + TRUNC_OBS_ID + "_kepler_v1_llc.fits"

In the above formula, TRUNC_OBS_ID is the observation ID *without* the "kegs" or "_lc" substrings, e.g., "220163813-c08" for the observation ID "kegs220163813-c08_lc".

## Description of Data Processing

Once the light curve file is located on disk, the time stamps and corrected fluxes are read.  The columns in the first FITS extension include "TIME", "FRAW", "FCOR1", "FCOR2", "FCOR3", "FCOR4", and "FCOR5", and are read by DataDelivery.  The time stamps are stored in a truncated BJD format, where the full barycentric Julian date is given by:

    BJD[i] = 2454833.0 + T[i]

In the above formula, "T" is the array of truncated BJD time stamps, stored as a column in the light curve file.  "FRAW" contains the non-detrended fluxes, while "FCOR1", "FCOR2", etc. contain the detrended fluxes using 1, 2, etc. cotrending basis vectors.  The units for fluxes inside these files are counts / sec within the aperture.
