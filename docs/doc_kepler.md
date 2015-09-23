# Documentation on Kepler Lightcurve Data Returned by DataDelivery

## Description of Kepler Lightcurve Data Formats

There are two main data products for Kepler: target pixel files (TPFs) and extracted lightcurves (often referred to as simply "lightcurves").  The TPF files are data cubes, and as such, are not supported by DataDelivery.  The lightcurve files are stored as FITS files, but there can be multiple FITS files associated with a given Kepler target.  First, a given target may be observed in a *short* cadence, a *long* cadence, or both.  The lightcurves for the cadences are located in separate FITS files.  In addition, there are separate FITS files for every *Quarter* the target was observed.  A "Quarter" in Kepler is a period of time, approximately three months long, during which the spacecraft was taking data with (nearly) no gaps in the observations.  After three months, the spacecraft needed to rotate 90 degrees, and another "Quarter" commenced.  There were a total of 18 Quarters during the lifetime of the Kepler mission.  A given Quarter has (almost always) a single *long* cadence file per observed target, and up to a few *short* cadence files per observed target.  The presence (and number) of files per Quarter for a target is encapsulated in that target's observation ID.  Note that counting of Quarters starts at zero, i.e., "Quarter 0" is the first Quarter in Kepler.  The formula for the observation ID is given by the following:

    observation ID = "kplr" + KIC_ID + "_" + CADENCE_STRING + "_Q" + QUARTER_ENCODING
    Example: kplr010593626_sc_Q001333333303333332

In the above example, the star KIC 010593626 was observed (in short cadence mode) zero times in Quarter 0, zero times in Quarter 1, one time in Quarter 2, three times in Quarter 3, etc.  For reference, here's the observation ID for the same star in *long* cadence mode:

    Example: kplr010593626_lc_Q111111111111111111

In this case, the star was observed in long cadence mode in each of the 18 possible Quarters.

## Description of How DataDelivery Locates Data

DataDelivery relies on parsing of the observation ID to determine which files to look for, and where to locate them on disk.  A variety of sanity checks (with associated error codes in the returned JSON object) are conducted on the observation ID to ensure it is properly parsed and the values DataDelivery finds within the observation ID are within expected parameters.  A look-up table within DataDelivery translates a given Quarter's value (1, 2, 3, etc.) into a list of potential file names to look for.  After searching for those files, it makes sure the number of files it found for that cadence+Quarter is the same as the number in the Quarter string part of the observation ID.

## Description of Data Processing

Once a set of files is located for a given target+cadence+Quarter, each FITS file is opened to obtain arrays of times and fluxes.  The data are stored as a data table in the first FITS extension.  The time stamps are stored in a truncated BJD format, where the full barycentric Julian date is given by:

    BJD[i] = BJDREFI + BJDREFF + TIME[i]

In the above formula, "BJDREFI" and "BJDREFF" are the integer and decimal components of the reference BJD date for the truncated time stamps.  These are located as header card values in the first FITS extension.  "TIME" is the array of truncated BJD time stamps, stored as a column in the first FITS extension.

There are two sets of fluxes commonly in demand: **SAP** and **PDCSAP** fluxes.  **SAP** (Simple Aperture Photometry) fluxes are the fluxes *before* additional detrending is applied.  **PDCSAP** (Pre-search Data Conditioning Simple Aperture Photometry) fluxes have had additional systematic uncertainties removed by applying corrections based on 16 "cotrending basis vectors", derived by analyzing hundreds of targets on the frame in "quiet" locations.  Many users will want to look at **PDCSAP** fluxes as a preview, but some astrophysical variation of interest can be removed during the PDCSAP correction process, so both fluxes are returned by DataDelivery so that the user may decide what they want to use.

### Special Note On Short Cadence Targets

Short-cadence data in particular can be quite large, with returned JSON strings over 100 MB in size.  This results in overly long wait times to return the data from these targets.  To help reduce the processing time for these targets, every Kepler short-cadence target has had their JSON string *pre-computed* and stored as text files on the server.  Once DataDelivery is given a short-cadence observation ID, it will first look for the cached JSON string on disk.  These are stored in their own directory on the server, where each observation ID's file name is given as:

    cache_file_name = OBSERVATION_ID + ".cache"

If the cache file is found, it will read in the text file and return the string stored inside it immediately to STDOUT.  If not, the fallback is to attempt to read the FITS file itself.
