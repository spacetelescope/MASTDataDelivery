# Documentation on HSLA Spectral Data Returned by DataDelivery

## Description of HSLA Spectra Data Formats

HSLA spectra are coadded based on the grating used.  The targets are separated into directories based on the grating used, which can be "G130M", "G160M", "G140L", or "FUVM", the latter being a splice of the G130M and G160M coadds.  Separate coadds exist for each lifetime position, while the "all" version contains a coadd across all the available lifetime positions.  In addition, the 1D spectra for each observation are available, named after the HST IPPPSSOOT ID, e.g., 'lbgu22z3q_x1d.fits.gz'.

## Description of How DataDelivery Locates Data

DataDelivery requires a *target* to identify the correct folder to search for FITS files.  If the request is at the coadd level, then the required *observation ID* should be set to 'hsla_coadd'.  This signals to DataDelivery that it should retrieve all FITS files with the word "coadd" inside the folder.  If the request is at the exposure-level, then set the *observation ID* to the HST IPPPSSOOT ID, and DataDelivery will retrieve that specific file inside the folder.

## Description of Data Processing

The spectral data are stored quite simply within each FITS file.  The wavelengths and fluxes are stored in a data table in the first FITS extension.  If it's a coadd file, DataDelivery returns the "wave", "fluxwgt", and "fluxwgt_err" columns.  If it's an exposure-level file, DataDelivery returns the "wavelength", "flux", and "error" columns from that file.  Each segment inside the exposure-level file is returned as a separate DataSeries.  If at the coadd-level, each coadd FITS file is returned as a separate DataSeries.  No additional processing or selection of data points to return is performed.
