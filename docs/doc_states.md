# Documentation on STATES Spectral Data Returned by DataDelivery

## Description of STATES Spectra Data Formats

STATES spectral data are stored in text files.  These files have a header containing extra information and column headers preceded by a pound sign ("#").  There are four columns of data, which nominally are the wavelengths, the delta wavelengths, (Rp/Rs)^2, and the uncertainties in (Rp/Rs)^2.  Only the wavelengths and (Rp/Rs)^2 are returned by DataDelivery.

## Description of How DataDelivery Locates Data

DataDelivery requires an *observation ID* to identify the correct STATES spectral file to read.  The name of the STATES spectral file is assumed to be the same as the observation ID with a ".txt" extension.  They are currently all assumed to be under a "transmission_spectra/" folder under the "states/" directory.

## Description of Data Processing

The spectral data are stored quite simply within each STATES spectral file.  The wavelengths and fluxes (the fluxes are taken as the (Rp/Rs)^2 values) are stored as columns in the text file.  No additional processing or selection of data points to return is performed.  The order of the columns is assumed to be immutable, and as (wavelength, delta wavelength, (Rp/Rs)^2, uncertainty in (Rp/Rs)^2).
