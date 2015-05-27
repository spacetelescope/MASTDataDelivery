from astropy.io import fits
import collections
from data_series import DataSeries
from parse_obsid_kepler import parse_obsid_kepler

#--------------------

def get_data_kepler(obsid):
    """
    Given a Kepler observation ID, returns the lightcurve data.

    :param obsid: The Kepler observation ID to retrieve the data from.

    :type obsid: str

    :returns: JSON -- The lightcurve data for this observation ID.

    Error codes:
    From parse_obsid_kepler:
    0 = No error parsing observation ID.
    1 = Could not unpack observation ID into three components.
    2 = Kepler ID in Observation ID string not within allowed bounds.
    3 = Kepler cadence type in Observation ID not an allowed value.
    4 = Kepler Q-code in Observation ID is not exactly 18 characters.
    5 = One or more files are missiong on disk based on the Q-code.
    From this module:
    6 = Could not open one or more FITS file for reading.
    """

    """ This defines a data point for a DataSeries object as a namedtuple. """
    data_point = collections.namedtuple('DataPoint', ['x','y'])
    
    """ Parse the obsID string to determine the paths+files to read.  Note: 
    this step will assign some of the error codes returned to the top level. """
    parsed_files_result = parse_obsid_kepler(obsid)

    if parsed_files_result.errcode == 0:
        """ For each file, read in the contents and create a return JSON 
        object. """
        all_plot_labels = ['']*2*len(parsed_files_result.files)
        all_plot_series = ['']*2*len(parsed_files_result.files)

        """ This error code will be used unless there's a problem reading any of
        the FITS files in the list. """
        errcode = 0
        for i,f in enumerate(parsed_files_result.files):
            try:
                with fits.open(f) as hdulist:
                    """ Extract time stamps and relevant fluxes. """
                    bjd = [float(x) for x in 
                           (float(hdulist[1].header["BJDREFI"]) + 
                            hdulist[1].header["BJDREFF"] + 
                            hdulist[1].data["TIME"])]
                    flux_sap = [float(x) for x in hdulist[1].data["SAP_FLUX"]]
                    flux_pdcsap = [float(x) for x in 
                                   hdulist[1].data["PDCSAP_FLUX"]]
                
                    """ Create the plot label and plot series for the SAP and 
                    PDCSAPfluxes. """
                    this_plot_label = ('KPLR_' + parsed_files_result.kepid + 
                                       ' ' + parsed_files_result.cadence.upper()
                                       + ' Q' + 
                                       parsed_files_result.quarters[i])
                    all_plot_labels[i*2] = this_plot_label + ' SAP'
                    all_plot_series[i*2] = [data_point(x=x, y=y) for x,y in 
                                            zip(bjd,flux_sap)]
                    all_plot_labels[i*2+1] = this_plot_label + ' PDCSAP'
                    all_plot_series[i*2+1] = [data_point(x=x, y=y) for x,y in 
                                              zip(bjd,flux_pdcsap)]
            except IOError:
                errcode = 6
                all_plot_labels[i*2] = ''
                all_plot_series[i*2] = []
                all_plot_labels[i*2+1] = ''
                all_plot_series[i*2+1] = []

        """ Create the return DataSeries object. """
        return_dataseries = DataSeries('kepler', obsid, all_plot_series, 
                                       all_plot_labels, 
                                       errcode)
    else:
        """ This is where an error DataSeries object would be returned. """
        return_dataseries = DataSeries('kepler', obsid, [], [], 
                                       parsed_files_result.errcode)
    
    """ Return the DataSeries object back to the calling module. """
    return return_dataseries

#--------------------
