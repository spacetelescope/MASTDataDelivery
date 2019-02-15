# Documentation on TESS Lightcurve Data Returned by DataDelivery

## Description of TESS Lightcurve Data Formats

There are two main postage-stamp-level data products for TESS: target pixel files (TPFs) and extracted lightcurves (often referred to as simply "lightcurves").  The TPF files are data cubes, and as such, are not supported by DataDelivery.  The lightcurve files are stored as FITS files.  TESS observes a part of the sky in 24x96 degree sections of the sky referred to as a **Sector**, approximately every 28 days.  Some parts of each Sector overlap, while Camera 4 in every Sector is in the same part of the hemisphere each Sector (a "continuous viewing zone").

The formula for the observation ID is given by the following:

    observation ID = "tess" + DATESTRING + "-" + SECTOR + "-" + TICID + "-" + SCID + "-" + CR

In the above formula, DATESTRING is the timestamp associated with the file, SECTOR is a string that begins with 's' then followed by a 4-digit, zero-padded sector number, TICID is the 16-digit, zero-padded TESS Input Catalog ID, SCID is the zero-padded, 4-digit identifier of the spacecraft configuration map used, and CR is a single-character string denoting the cosmic ray mitigation procedure.  An example of a full observation ID is:

    tess2018234235059-s0002-0000000002733208-0121-s

## Description of How DataDelivery Locates Data

DataDelivery relies on parsing of the observation ID to determine which files to look for, and where to locate them on disk.  A variety of sanity checks (with associated error codes in the returned JSON object) are conducted on the observation ID to ensure it is properly parsed and the values DataDelivery finds within the observation ID are within expected parameters.

The FITS files are stored in a subdirectory path, based on the observation ID, with the following format:

    subdir_path = s<####>/<####>/<####>/<####>/<####>/

In the above formula, the first part is the 4-digit, zero-padded Sector number, the next four parts are the first, second, third, and fourth groups of digits (in groups of 4) of the 16-digit, zero-padded TIC ID.  As an example, the observation ID "tess2018234235059-s0002-0000000002733208-0121-s" would lie in a subdirectory path of:

    s0002/0000/0000/0273/3208/

## Description of Data Processing

Once a FITS file is located for a given target, it's opened for reading to obtain arrays of times and fluxes.  The data are stored as a data table in the first FITS extension.  The time stamps are stored in a truncated BJD format, where the full barycentric Julian date is given by:

    BJD[i] = BJDREFI + BJDREFF + TIME[i]

In the above formula, "BJDREFI" and "BJDREFF" are the integer and decimal components of the reference BJD date for the truncated time stamps.  These are located as header card values in the first FITS extension.  "TIME" is the array of truncated BJD time stamps, stored as a column in the first FITS extension.

There are two sets of fluxes commonly in demand: **SAP** and **PDCSAP** fluxes.  **SAP** (Simple Aperture Photometry) fluxes are the fluxes *before* additional detrending is applied.  **PDCSAP** (Pre-search Data Conditioning Simple Aperture Photometry) fluxes have had additional systematic uncertainties mitigated.  Many users will want to look at **PDCSAP** fluxes as a preview, but some astrophysical variation of interest can be removed during the PDCSAP correction process, so both fluxes are returned by DataDelivery so that the user may decide what they want to use.
