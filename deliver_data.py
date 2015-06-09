import argparse
from get_data_kepler import get_data_kepler
import json

#--------------------
def json_encoder(obj):
    """
    Defines a method to use when serializing into JSON.
    """
    return obj.__dict__
#--------------------


#--------------------
def deliver_data(missions, obsids):
    """
    Given a list of mission + obsid strings, returns the lightcurve and/or 
    spectral data from each of them.

    :param missions: The list of missions where the data come from, one per 
    'obsid'.
    
    :type missions: list

    :param obsids: The list of observation IDs to retrieve the data from.

    :type obsids: list

    :returns: JSON -- The lightcurve or spectral data from the requested data 
    products.

    """
    
    """ The length of the 'missions' and 'obsids' lists must be equal. """
    if len(missions) != len(obsids):
        raise IOError("Number of 'missions' must equal the number of 'obsids'.")

    """ Make sure the input data are sorted based on the obsids, so that the"
    " input is order-independent. """
    sort_indexes = sorted(range(len([x+'-'+y for x,y in zip(missions,obsids)])),
                          key=lambda k: [x+'-'+y for x,y in 
                                         zip(missions,obsids)][k])
    missions = [missions[x] for x in sort_indexes]
    obsids = [obsids[x] for x in sort_indexes]

    """ Each mission+obsID pair will have a DataSeries object returned, so make
    a list to store them all in. """
    all_data_series = []

    for mission, obsid in zip(missions,obsids):
        if mission == 'kepler':
            this_data_series = get_data_kepler(obsid)
        else:
            """ This is where other mission-specific modules will go. """
            pass

        """ Append this DataSeries object to the list. """
        all_data_series.extend([this_data_series])

    """ Return the list of DataSeries objects as a JSON string. """
    return json.dumps(all_data_series, ensure_ascii=True, check_circular=True,
                      encoding="utf-8", default=json_encoder)
#--------------------

#--------------------
def setup_args():
    """
    Set up command-line arguments and options.

    :returns: ArgumentParser -- Stores arguments and options.
    """
    parser = argparse.ArgumentParser(description="Retrieves data "
                                     "from MAST and delivers the contents "
                                     "(spectra or lightcurves) as a JSON.")

    parser.add_argument("-m" "--missions", action="store", dest="missions", 
                        type=str.lower, nargs='+',
                        choices=['befs',
                                 'euve',
                                 'fuse',
                                 'galex',
                                 'hst',
                                 'hut',
                                 'iue',
                                 'k2',
                                 'kepler',
                                 'tues',
                                 'wuppe'],
                        help="Required: The mission(s) where this data comes "
                        "from.  There must be the same number of 'obsid' "
                        "values.")

    parser.add_argument("-o", "--obsids", action="store", dest="obsids",
                        type=str.lower, nargs='+',
                        help="[Required] The observation ID(s) to retrieve data"
                        " from.  There must be the same number of 'missions' "
                        "values.")

    return parser
#--------------------

#--------------------
if __name__ == "__main__":

    """ Setup command-line arguments. """
    args = setup_args().parse_args()

    json_string = deliver_data(args.missions, args.obsids)

    """ Print the return JSON object to STDOUT. """
    print json_string

#--------------------
