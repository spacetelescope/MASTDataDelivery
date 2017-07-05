# Documentation on HLSP_K2POLAR Lightcurve Data Returned by DataDelivery

## Description of HLSP_K2POLAR Lightcurve Data Formats

HLSP_K2POLAR are high level science products contributed by Susana Barros et al.  The MAST HLSP page is located at https://archive.stsci.edu/prepds/polar/.  Not every K2 target has a POLAR lightcurve, for example, short cadence targets are not included in POLAR.  The extracted, detrended lightcurves are stored in FITS files, one per K2 target.  Each target has both a **detrended** and a **detrended + filtered** version of the fluxes available, where the **detrended** fluxes have thruster firings and other systematics mitigated, while the **filtered** fluxes have also had stellar activity removed.

The FITS file has 2 extensions: the primary HDU with just a header, the data extension with the detrended light curve, and an extension with the detrended+filtered light curve. The detrended extension (first extension) consists of the following columns:

* TIME - time array (BJD - 2400000.0)
* FLUX - the detrended flux array, normalized
* FLUXERR - error of the normalized, detrended fluxes

The filtered extension (second extension) consits of the following columns:

* FILTIME - time array (BJD - 2400000.0), different from time array in detrended extension
* FILFLUX - the detrended and filtered flux array, normalized
* FILFLUXERR - error of the normalized, detrended and filtered fluxes

## Description of How DataDelivery Locates Data

DataDelivery only requires an observation ID to uniquely identify the FITS file to read from disk.  The HLSP_K2POLAR observation IDs are stored in a subdirectory path that has the following format:

    subdir_path = c<##>/<####00000>/<#####>/

In the above formula, the first part is the 2-digit campaign number, the second part is the first four digits of the EPIC (target) ID, and the last part is the final five digits of the EPIC ID.  As an example, the observation ID "k2polar201172129-c01_lc" would lie in a subdirectory path of:

    c01/201100000/72129/

The names of the FITS files are given by the following formula:

    "hlsp_polar_k2_lightcurve_" + TRUNC_OBS_ID + "_kepler_v1_llc.fits"

In the above formula, TRUNC_OBS_ID is the observation ID *without* the "k2polar" or "_lc" substrings, e.g., "201172129-c01" for the observation ID "201172129-c01_lc".

## Description of Data Processing

Once the FITS file is located on disk, the time stamps, detrended fluxes, and detrended+filtered fluxes are read.  The time stamps are stored in a truncated BJD format, where the full barycentric Julian date is given by:

    BJD[i] = TIME[i] + 2400000.0

Similarly, the **detrended** and **detrended+filtered** fluxes are stored as columns in the data table of the first and second FITS extensions, respectively.  Times or fluxes that are non-finite (NaN's) are removed.  No additional processing is performed on the fluxes, and no filtering based on quality flags or other selection criteria is performed.
