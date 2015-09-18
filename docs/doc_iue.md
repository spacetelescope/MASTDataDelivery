# Documentation on IUE Spectral Data Returned by DataDelivery

## Description of IUE Spectra Data Formats

IUE spectral data come in a few different formats, depending on what *aperture size* was used and what *dispersion* the data come from.  A given spectrum may be **low** or **high** dispersion.  The high dispersion spectra come from an echelle grating, and consequently contain multiple orders that overlap in wavelength space.  The low dispersion spectra come from just a cross-disperser grating, and hence there is just a single wavelength series.  There are some observation IDs that have both a low and high dispersion spectrum available.  Those are referred to as *double dispersion* data, but the low and high dispersion spectra are stored in different FITS files on disk.  Similarly to the choice of two different dispersion values, a given spectrum may be taken using the **small** or **large** aperture size.  There are some observation IDs that have both a small and large aperture spectrum available.  Those are referred to as *double aperture* data, but unlike the *double dispersion* spectra, the *double aperture* data live in the same FITS file on disk.  As a side note, only **low** dispersion spectra may be *double aperture* data.

## Description of How DataDelivery Locates Data

DataDelivery requires an *observation ID* and a *filter value* to identify the correct FITS file to read.  The filter column identifies whether to retrieve the low or high dispersion FITS file for this observation ID.  This is necessary because, as mentioned above, some observation IDs are *double dispersion* and hence the observation ID by itself is not sufficient to determine which file to read.  A *low dispersion* file will always end in "mxlo.gz", while a *high dispersion* file will always end in "mxhi.gz".  DataDelivery uses the final seven characters in the file name to identify whether it is a low or high dispersion spectrum.

## Description of Data Processing

### Low Dispersion Spectra

Low dispersion spectra are the only ones that can have both a *small* and *large* aperture spectrum inside it.  The spectra are located in the first extension of the FITS file.  If the file represents a *double aperture* observation ID, both the small and large aperture spectra are in the same FITS file (the first row corresponds to the large aperture, the second to the small aperture).  For *double aperture* observation IDs, DataDelivery will treat them as separate missions/obsIDs, so for example, if "lwr01244" is a *double aperture* observation ID, the returned JSON strings will be as if there were two observation IDs given on input, one containing the *small* aperture and one containing the *large* aperture.

The wavelength values are not stored directly in the FITS file.  Rather, a starting wavelength value and a step size are given, and they are used to generate the array of wavelength values.  The array of wavelength values is constructed using the following formula.

    for i=0...n_wls:
        wl_i = wl_start + i*wl_step

In the formula for wavelength above, *n_wls* represents the number of data points for each aperture size, while *wl_start* is the starting wavelength value in Angstroms and *wl_step* is the (constant) step size of each subsequent wavelength value in Angstroms.  These are stored in the first header extension: if this is a *double aperture* observation, then these values are each stored as 2-element arrays.

The flux values are also stored in the first extension.  If this is a *double aperture* observation then the fluxes are stored as a 2-D table, otherwise the fluxes are stored in a simple array of length *n_wls*.  The returned spectrum trims out any (wavelength,flux) pairs where the flux is exactly 0.0, since these are points that lie outside the absolute calibration wavelength range.  A complete description of the FITS file format for *low dispersion* spectra can be found at http://archive.stsci.edu/iue/manual/newsips/node154.html#SECTION001480000000000000000

### High Dispersion Spectra

High dispersion spectra always have a single aperture inside their FITS file: either *small* or *large*.  However, they require significantly more processing than the low dispersion spectra because of the multiple echelle orders and treatment of their overlap in wavelength space.  The *high dispersion* data are stored differently from the *low dispersion* data.  The first extension consists of 17 fields, and each field contains one entry per echelle order.  Any of the 17 fields that are vectors have a fixed length of 768 elements.  Zeroes are used to pad the beginning and ends of these vectors where data do not exist for that particular order.  The array of wavelength values is constructed using the following formula.

    for i=0...n_wls:
        wl_i = wl_start + i*wl_step

In the formula for wavelength above, *n_wls* represents the number of data points for this order, while *wl_start* is the starting wavelength value in Angstroms and *wl_step* is the (constant) step size of each subsequent wavelength value in Angstroms.  An important note is that the *wl_start* is **not** the wavelength value corresponding to the first element in the 768-element vectors.  Rather, it is the wavelength value corresponding to the **starting pixel**.  The starting pixel value is stored as one of the 17 fields for each order.  **NOTE:** the starting pixel is indexed starting at one, not zero, so for 0-indexed languages (like python) you must start at the "starting pixel -1" position in the vectors.  The fluxes that correspond to each wavelength value are thus extracted using the following formula (keeping in mind that python slicing requires you to go one index beyond your endpoint).


    fls = fluxes[s_pix-1]:fluxes[s_pix+n_wls]

Once the full set of wavelengths and fluxes are extracted, further selection is applied using the *quality flags* assigned to each flux value, which are themselves stored as one of the 17 fields in the header extension.  During the remaining steps, we partially follow the description of order-combining IUE spectra given by [Solano](iue_ordercombine.pdf).  For each order, only (wl,fl) pairs that have a quality flag > -16384 are kept.  If an order has all flux values with quality flag <= -16384, that order is not included at all.  A description of quality flag codes can be found at http://archive.stsci.edu/iue/manual/newsips/node20.html#SECTION00500000000000000000.

After the wavelengths and fluxes with good quality flags are extracted for all the orders, they are order-combined into a single, contiguous array.  Given an order "m" and an adjacent order "m-1", the "cut wavelength" is calculated following [Solano's](iue_ordercombine.pdf) Equations 1 and 2.  The cut wavelength depends on the camera that was used for that observation.  All points with wavelength wl1 <= the cut wavelength from order "m", and all points with wavelength wl2 > the cut wavelength from order "m-1" are kept.  The figure below demonstrates how the cut wavelength concept works for two adjacent orders.

![IUE Order Combine Example](iue_ordercomb.png?raw=true)

After the orders have been combined into a contiguous array, the spectrum is resampled onto a linear, evenly-spaced wavelength grid.  For the SWP camera the final bin size is set to 0.05 Angstroms, while the LWP and LWR cameras use a final bin size of 0.10 Angstroms.  If there are any gaps in the spectrum (due to bad orders or other pieces that were not included due to bad quality flags) the spectrum is split into "subspectra" before creating the wavelength grids.

For each subspectrum, a grid of wavelengths are calculated, starting at the min. wavelength value and ending at the maximum wavelength value in the spectrum, where the wavelength spacing is defined as the (oversampled) bin size.  The bins are oversampled by a factor of 10, so the initial wavelength grid is in step sizes of 0.005 or 0.01, depending on which camera the spectrum is coming from.  The spectrum is then linearly interpolated onto this wavelength grid.  Then the interpolated subpsectrum is binned back down by a factor of 10 to achieve the final, desired wavelength grid.  This is accomplished by taking the mean of each set of ten wavelengths and fluxes.  If the subspectrum is not a multiple of 10, NaN values are appended to the end of the subspectrum array.  The figure below is a zoomed-in portion of a subspectrum to demonstrate how the resampling and binning works.

![IUE Linear Interpolation Example](iue_resample_interp.png?raw=true)

The figure below shows how gaps in the spectra are **not** interpolated over (the blue vertical lines identify where a gap stars).  The green lines between gaps is just a visual artifact of plotting the series, connecting the points between gaps, but one will note that there are not any **actual** points in the gaps, as desired.

![IUE Subspectrum Identification Example](iue_resample_subspec.png?raw=true)
