# Documentation on HLSP_K2GAP Lightcurve Data Returned by DataDelivery

## Description of HLSP_K2GAP Lightcurve Data Formats

HLSP_K2GAP are high level science products contributed by Dennis Stello and team.  The MAST HLSP page is located at https://archive.stsci.edu/prepds/k2gap/.  Not every K2 target has a K2GAP lightcurve, for example, short cadence targets are not included in K2GAP.  In fact, K2GAP is an asteroseismology project, so they only create light curves for red giant stars.  Their starting point are, in fact, the K2SFF detrended light curves, themselves an HLSP at MAST.  They perform some additional processing on them, however, so they provide those light curves as a text table in their HLSP, one file per target.  The text table consists of two columns, the time in Kepler BJD format (BJD - 2454833.0) and their version of the normalized, detrended flux.  It is this flux that they conduct their asteroseismology on.  They also provide the power spectrum of this light curve as a separate file: DataDelivery currently only read and provides back the detrended light curve, it does not provide data from the power spectrum file at this time.

## Description of How DataDelivery Locates Data

DataDelivery only requires an observation ID to uniquely identify the K2GAP file to read from disk.  The HLSP_K2GAP observation IDs are stored in a subdirectory path that has the following format:

    subdir_path = c<##>/<####00000>/<#####>/

In the above formula, the first part is the 2-digit campaign number, the second part is the first four digits of the EPIC (target) ID, and the last part is the final five digits of the EPIC ID.  As an example, the observation ID "k2gap201121245-c01_lc" would lie in a subdirectory path of:

    c01/201100000/21245/

The names of the light curve files are given by the following formula:

    "hlsp_k2gap_k2_lightcurve_" + TRUNC_OBS_ID + "_kepler_v1_ts.txt"

In the above formula, TRUNC_OBS_ID is the observation ID *without* the "k2gap" or "_lc" substrings, e.g., "201121245-c01" for the observation ID "k2gap201121245-c01_lc".

## Description of Data Processing

Once the light curve file is located on disk, the time stamps and corrected fluxes are read.  The time stamps are stored in a truncated BJD format, where the full barycentric Julian date is given by:

    BJD[i] = 2454833.0 + T[i]

In the above formula, "T" is the array of truncated BJD time stamps, stored as a column in the light curve file.
