"""
.. module:: deliver_data

   :synopsis: Reads spectral or lightcurve data from MAST missions and returns
              them as JSON strings.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import argparse
from get_data_hlsp_k2sff import get_data_hlsp_k2sff
from get_data_hlsp_k2varcat import get_data_hlsp_k2varcat
from get_data_iue import get_data_iue
from get_data_kepler import get_data_kepler
import json

from mpl_get_data_euve import mpl_get_data_euve
from mpl_get_data_fuse import mpl_get_data_fuse
from mpl_get_data_galex import mpl_get_data_galex
from mpl_get_data_hut import mpl_get_data_hut
from mpl_get_data_wuppe import mpl_get_data_wuppe

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

    # The length of the 'missions' and 'obsids' lists must be equal.
    if len(missions) != len(obsids):
        raise IOError("Number of 'missions' must equal the number of 'obsids'.")

    # Make sure the input data are sorted based on the obsids, so that the
    # input is order-independent.
    sort_indexes = sorted(range(len([x+'-'+y for x, y in
                                     zip(missions, obsids)])), key=
                          lambda k: [x+'-'+y for x, y in
                                     zip(missions, obsids)][k])
    missions = [missions[x] for x in sort_indexes]
    obsids = [obsids[x] for x in sort_indexes]

    # Each mission + obsID pair will have a DataSeries object returned, so make
    # a list to store them all in.
    all_data_series = []

    for mission, obsid in zip(missions, obsids):
        if mission == "euve":
            this_data_series = mpl_get_data_euve(obsid)
        if mission == "hlsp_k2sff":
            this_data_series = get_data_hlsp_k2sff(obsid)
        if mission == "hlsp_k2varcat":
            this_data_series = get_data_hlsp_k2varcat(obsid)
        if mission == "fuse":
            this_data_series = mpl_get_data_fuse(obsid)
        if mission == "galex":
            this_data_series = mpl_get_data_galex(obsid)
        if mission == "hut":
            this_data_series = mpl_get_data_hut(obsid)
        if mission == "iue":
            this_data_series = get_data_iue(obsid)
        if mission == 'kepler':
            this_data_series = get_data_kepler(obsid)
        if mission == "wuppe":
            this_data_series = mpl_get_data_wuppe(obsid)

        # Append this DataSeries object to the list.
        all_data_series.extend([this_data_series])

    # Return the list of DataSeries objects as a JSON string.
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
                                 'hlsp_k2sff',
                                 'hlsp_k2varcat',
                                 'hst',
                                 'hut',
                                 'iue',
                                 'kepler',
                                 'tues',
                                 'wuppe'],
                        help="Required: The mission(s) where this data comes "
                        "from.  There must be the same number of 'obsid' "
                        "values.")

    parser.add_argument("-o", "--obsids", action="store", dest="obsids",
                        type=str, nargs='+',
                        help="[Required] The observation ID(s) to retrieve data"
                        " from.  There must be the same number of 'missions' "
                        "values.")

    return parser
#--------------------

#--------------------
if __name__ == "__main__":

    # Setup command-line arguments.
    ARGS = setup_args().parse_args()

    JSON_STRING = deliver_data(ARGS.missions, ARGS.obsids)

    # Print the return JSON object to STDOUT.
    print JSON_STRING
#--------------------
