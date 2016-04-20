# Documentation on HLA/HSC Grism Spectral Data Returned by DataDelivery

## Description of HLA/HSC Spectra Data Formats

Extracted ACS or NICMOS data are stored in FITS files ending in "SPEC1D.FITS".  The wavelengths and fluxes are stored in the first extension.  The parent (unextracted) spectra are stored in FITS files ending in "SPEC2D.FITS".

## Description of How DataDelivery Locates Data

DataDelivery requires an *observation ID* to identify the correct FITS file to read.  If the observation ID ends with "SPEC1D.FITS" then it will attempt to read in the file and return the wavelengths and fluxes.  If it ends with "SPEC2D.FITS" it will return an error JSON identifying the spectrum is an unextracted 2D spectrum.

## Description of Data Processing

The spectral data are stored quite simply within each FITS file.  The wavelengths and fluxes are stored in a data table in the first FITS extension, in columns called "wave" and "flux", respectively.  No additional processing or selection of data points to return is performed.
