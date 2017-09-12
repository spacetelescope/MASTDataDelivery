"""
.. module:: deliver_data

   :synopsis: Reads spectral or lightcurve data from MAST missions and returns
              them as JSON strings.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import argparse
import json
import os
from data_series import DataSeries
from get_data_galex import get_data_galex
from get_data_hlsp_k2everest import get_data_hlsp_k2everest
from get_data_hlsp_k2gap import get_data_hlsp_k2gap
from get_data_hlsp_k2polar import get_data_hlsp_k2polar
from get_data_hlsp_k2sc import get_data_hlsp_k2sc
from get_data_hlsp_k2sff import get_data_hlsp_k2sff
from get_data_hlsp_k2varcat import get_data_hlsp_k2varcat
from get_data_hsc_grism import get_data_hsc_grism
from get_data_hsla import get_data_hsla
from get_data_iue import get_data_iue
from get_data_k2 import get_data_k2
from get_data_kepler import get_data_kepler

from mpl_get_data_befs import mpl_get_data_befs
from mpl_get_data_euve import mpl_get_data_euve
from mpl_get_data_fuse import mpl_get_data_fuse
from mpl_get_data_hst import mpl_get_data_hst
from mpl_get_data_hut import mpl_get_data_hut
from mpl_get_data_tues import mpl_get_data_tues
from mpl_get_data_wuppe import mpl_get_data_wuppe

# Default location of Kepler cache files.
CACHE_DIR_DEFAULT = (os.path.pardir + os.path.sep + os.path.pardir +
                     os.path.sep + "missions" + os.path.sep + "kepler" +
                     os.path.sep + "lightcurves" + os.path.sep + "cache" +
                     os.path.sep)
FILTERS_DEFAULT = None
TARGET_DEFAULT = None
URLS_DEFAULT = None

#--------------------
def json_encoder(obj):
    """
    Defines a method to use when serializing into JSON.
    """
    return obj.__dict__
#--------------------

#--------------------
def json_too_big_object(mission, obsid):
    """
    Returns a default JSON object when the requested data is too large for the
    client to handle.

    :param mission: The mission where the data come from.

    :type mission: str

    :param obsid: The observation ID to retrieve the data from.

    :type obsid: str

    :returns: JSON -- The default JSON to return when the requested data is too
    large for the MAST Portal to handle.  Note the error code for this scenario
    is set to 99.
    """
    # Define the custom error code.
    errcode = 99
    # Crate the return list of data series.
    all_data_series = [DataSeries(mission, obsid, [], [], [], [], errcode)]
    # Create the default return JSON object.
    return_json = json.dumps(all_data_series, ensure_ascii=False,
                             check_circular=False, encoding="utf-8",
                             default=json_encoder)
    return return_json
#--------------------


#--------------------
def deliver_data(missions, obsids, filters=FILTERS_DEFAULT, urls=URLS_DEFAULT,
                 targets=TARGET_DEFAULT, cache_dir=CACHE_DIR_DEFAULT):
    """
    Given a list of mission + obsid strings, returns the lightcurve and/or
    spectral data from each of them.

    :param missions: The list of missions where the data come from, one per
    'obsid'.

    :type missions: list

    :param obsids: The list of observation IDs to retrieve the data from.

    :type obsids: list

    :param filters: The list of FILTER values for the observation ID, one per
    'obsid'.

    :type filters: list

    :param cache_dir: Directory containing Kepler cache files.

    :param urls: The list of preview plot URLs for the observation ID, one per
    'obsid'.

    :type urls: list

    :param targets: The list of target names, one per 'obsid'.

    :type targets: list

    :type cache_dir: str

    :returns: JSON -- The lightcurve or spectral data from the requested data
    products.
    """

    # If the list of filters is not supplied (because not all missions use it),
    # then just default to a list of single whitespace strings.
    if filters is None:
        filters = [' '] * len(missions)

    # If the list of URLs is not supplied (because not all missions use it),
    # then just default to a list of single whitespace strings.
    if urls is None:
        urls = [' '] * len(missions)

    # If the list of targets is not supplied (because not all missions use it),
    # then just default to a list of single whitespace strings.
    if targets is None:
        targets = [' '] * len(missions)

    # There must be something supplied for 'mission' and 'obsid' supplied.
    if missions is None or obsids is None:
        raise IOError("Both 'missions' and 'obsids' must be supplied.")

    # The length of the 'missions' and 'obsids' lists must be equal.
    if len(missions) != len(obsids):
        raise IOError("Number of 'missions' must equal the number of 'obsids'.")

    # Make sure the input data are sorted based on the obsids, so that the
    # input is order-independent.
    sort_indexes = sorted(range(len([x+'-'+y+'-'+z+'-'+u for x, y, z, u in
                                     zip(missions, obsids, filters, urls)])),
                          key=
                          lambda k: [x+'-'+y+'-'+z+'-'+u for x, y, z, u in
                                     zip(missions, obsids, filters, urls)][k])
    missions = [missions[x] for x in sort_indexes]
    obsids = [obsids[x] for x in sort_indexes]
    filters = [filters[x] for x in sort_indexes]
    urls = [urls[x] for x in sort_indexes]
    targets = [targets[x] for x in sort_indexes]

    # This defines the maximum allowed size of a return JSON string
    # (roughly in MB).
    max_json_size = 64.E6

    # Each mission + obsID pair will have a DataSeries object returned, so make
    # a list to store them all in.
    all_data_series = []

    for mission, obsid, filt, url, targ in zip(missions, obsids, filters,
                                               urls, targets):
        if mission == "befs":
            this_data_series = mpl_get_data_befs(obsid)
        if mission == "euve":
            this_data_series = mpl_get_data_euve(obsid)
        if mission == "fuse":
            this_data_series = mpl_get_data_fuse(obsid)
        if mission == "galex":
            this_data_series = get_data_galex(obsid, filt, url.strip())
        if mission == "hlsp_k2everest":
            this_data_series = get_data_hlsp_k2everest(obsid)
        if mission == "hlsp_k2gap":
            this_data_series = get_data_hlsp_k2gap(obsid)
        if mission == "hlsp_k2polar":
            this_data_series = get_data_hlsp_k2polar(obsid)
        if mission == "hlsp_k2sc":
            this_data_series = get_data_hlsp_k2sc(obsid)
        if mission == "hlsp_k2sff":
            this_data_series = get_data_hlsp_k2sff(obsid)
        if mission == "hlsp_k2varcat":
            this_data_series = get_data_hlsp_k2varcat(obsid)
        if mission == "hsc_grism":
            this_data_series = get_data_hsc_grism(obsid)
        if mission == "hsla":
            this_data_series = get_data_hsla(obsid, targ)
        if mission == "hst":
            this_data_series = mpl_get_data_hst(obsid)
        if mission == "hut":
            this_data_series = mpl_get_data_hut(obsid)
        if mission == "iue":
            this_data_series = get_data_iue(obsid.lower(), filt)
        if mission == "k2":
            this_data_series = get_data_k2(obsid)
        if mission == 'kepler':
            # If short cadence we use cached files for efficiency.
            if "_sc_" in obsid:
                # Make sure cache_dir is marked.
                cache_dir = os.path.join(cache_dir, '')
                cache_file = cache_dir + obsid + ".cache"
                # Open the cache file and return that string.
                if os.path.isfile(cache_file):
                    with open(cache_file, 'r') as ifile:
                        return_string = ifile.readlines()[0]
                        if len(return_string) <= max_json_size:
                            return return_string
                        else:
                            return json_too_big_object(mission, obsid)
                else:
                    # Cache file is missing, fall back to creating from FITS.
                    this_data_series = get_data_kepler(obsid)
            else:
                this_data_series = get_data_kepler(obsid)
        if mission == "tues":
            this_data_series = mpl_get_data_tues(obsid)
        if mission == "wuppe":
            this_data_series = mpl_get_data_wuppe(obsid)

        # Append this DataSeries object to the list.  Some IUE obsIDs (those
        # that are double-aperture) return already as a list of DataSeries, so
        # check whether it's a list or not before extending.
        if not isinstance(this_data_series, list):
            this_data_series = [this_data_series]
        all_data_series.extend(this_data_series)

    # Return the list of DataSeries objects as a JSON string.
    return_string = json.dumps(all_data_series, ensure_ascii=False,
                               check_circular=False, encoding="utf-8",
                               default=json_encoder)
    if len(return_string) <= max_json_size:
        return return_string
    else:
        return json_too_big_object(', '.join(missions), ', '.join(obsids))
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
                                 'hlsp_k2everest',
                                 'hlsp_k2gap',
                                 'hlsp_k2polar',
                                 'hlsp_k2sc',
                                 'hlsp_k2sff',
                                 'hlsp_k2varcat',
                                 'hsc_grism',
                                 'hsla',
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
                        type=str, nargs='+',
                        help="[Required] The observation ID(s) to retrieve data"
                        " from.  There must be the same number of 'missions' "
                        "values.")

    parser.add_argument("-c", "--cdir", action="store", dest="cache_dir",
                        type=str, default=CACHE_DIR_DEFAULT, help="Location of"
                        " Kepler cache files.  Do not specify this unless you"
                        " have a specific need to.  The default value should be"
                        " correct for most use cases.")

    parser.add_argument("-f", "--filters", action="store", dest="filters",
                        type=str, nargs='+', default=FILTERS_DEFAULT,
                        help="Some missions"
                        " require additional data be specified beyond the"
                        " observation ID to uniquely identify what spectrum to"
                        " return (e.g., IUE).  The FILTER column is one"
                        " parameter used in this case.  Missions that do not"
                        " require the FILTER column to be specified will ignore"
                        " this parameter, whether it is provided on input or"
                        " not.")

    parser.add_argument("-t", "--target", action="store", dest="target",
                        type=str, nargs="+", default=TARGET_DEFAULT,
                        help="Some missions require additional data to be"
                        " specified beyond the observation ID to uniquely"
                        " identify what spectrum to return. The TARGET column"
                        " is one parameter used in this case.  Missions that do"
                        " not require the TARGET column to be specified will"
                        " ignore this parameter, whether it is provided on"
                        " input or not.")

    parser.add_argument("-u", "--urls", action="store", dest="urls",
                        type=str, nargs='+', default=URLS_DEFAULT,
                        help="Some missions"
                        " require additional data be specified beyond the"
                        " observation ID to uniquely identify what spectrum to"
                        " return (e.g., GALEX).  The preview URL column is one"
                        " parameter used in this case.  Missions that do not"
                        " require the URL column to be specified will ignore"
                        " this parameter, whether it is provided on input or"
                        " not.")

    return parser
#--------------------

#--------------------
if __name__ == "__main__":

    # Setup command-line arguments.
    ARGS = setup_args().parse_args()

    JSON_STRING = deliver_data(ARGS.missions, ARGS.obsids, filters=ARGS.filters,
                               urls=ARGS.urls, targets=ARGS.target,
                               cache_dir=ARGS.cache_dir)

    # Print the return JSON object to STDOUT.
    print JSON_STRING
#--------------------
