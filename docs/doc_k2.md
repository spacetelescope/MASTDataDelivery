# Documentation on K2 Lightcurve Data Returned by DataDelivery

## Description of K2 Lightcurve Data Formats

There are two main data products for K2: target pixel files (TPFs) and extracted lightcurves (often referred to as simply "lightcurves").  The TPF files are data cubes, and as such, are not supported by DataDelivery.  The lightcurve files are stored as FITS files.  A given target may be observed in a *short* cadence, a *long* cadence, or both.  The lightcurves for the cadences are located in separate FITS files.  Each part of the sky is visited by the K2 telescope for approximately 80 days, referred to as a **Campaign**, after which a new part of the sky is visited.

The formula for the observation ID is given by the following:

    observation ID = "ktwo" + EPIC_ID + "-c" + CAMPAIGN_NUM + "_" + CADENCE_STRING

In the above formula, EPIC_ID is the ID number from the EPIC catalog, CAMPAIGN_NUM is the two-digit, zero-padded Campaign number (the first one starts at **zero**), and CADENCE_STRING is either "lc" for *long cadence* or "sc" for *short cadence*.  Here's an example observation ID for the long cadence lightcurve of EPIC target 205901354, observed in Campaign 3.

    ktwo205901354-c03_lc

Note: Campaigns 0-2 do not (as of 23 Sept. 2015) have extracted lightcurves provided by the mission.

## Description of How DataDelivery Locates Data

DataDelivery relies on parsing of the observation ID to determine which files to look for, and where to locate them on disk.  A variety of sanity checks (with associated error codes in the returned JSON object) are conducted on the observation ID to ensure it is properly parsed and the values DataDelivery finds within the observation ID are within expected parameters.

The FITS files are stored in a subdirectory path, based on the observation ID, with the following format:

    subdir_path = c<#>/<####00000>/<##000>/

In the above formula, the first part is the campaign number (**not zero-padded**), the second part is the first four digits of the EPIC (target) ID, and the last part is the 5th and 6th digits of the EPIC ID.  As an example, the observation ID "ktwo205901354-c03_lc" would lie in a subdirectory path of:

    c3/205900000/01000

## Description of Data Processing

Once a FITS file is located for a given target, it's opened for reading to obtain arrays of times and fluxes.  The data are stored as a data table in the first FITS extension.  The time stamps are stored in a truncated BJD format, where the full barycentric Julian date is given by:

    BJD[i] = BJDREFI + BJDREFF + TIME[i]

In the above formula, "BJDREFI" and "BJDREFF" are the integer and decimal components of the reference BJD date for the truncated time stamps.  These are located as header card values in the first FITS extension.  "TIME" is the array of truncated BJD time stamps, stored as a column in the first FITS extension.

There are two sets of fluxes commonly in demand: **SAP** and **PDCSAP** fluxes.  **SAP** (Simple Aperture Photometry) fluxes are the fluxes *before* additional detrending is applied.  **PDCSAP** (Pre-search Data Conditioning Simple Aperture Photometry) fluxes have had additional systematic uncertainties mitigated.  Many users will want to look at **PDCSAP** fluxes as a preview, but some astrophysical variation of interest can be removed during the PDCSAP correction process, so both fluxes are returned by DataDelivery so that the user may decide what they want to use.
