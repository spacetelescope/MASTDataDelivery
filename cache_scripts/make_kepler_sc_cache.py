"""
This script is used to generate cached results of Kepler short cadence data for all targets observed in that mode.  It's in this repository for archival purposes, but is not part of the main DataDelivery package.
"""

import os
import deliver_data

def make_kepler_sc_cache():
    # Base output directory.
    cache_dir = '/ifs/public/mast/kepler/lightcurves/cache/'
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)

    mission = "kepler"

    # Read in master list of Kepler IDs.
    with open("Kepler_Lightcurves.csv", 'r') as ifile:
        obsids = ifile.readlines()
    obsids = [x.strip() for x in obsids]
    nids = len(obsids)

    for i,o in enumerate(obsids):
        print str(i+1) + '/' + str(nids)
        
        if "_sc_" in o:
            # Create the JSON string.
            json_str = deliver_data.deliver_data([mission], [o], '')
        
            # Write JSON string to output file.
            with open(cache_dir + o + ".cache", 'w') as ofile:
                ofile.write(json_str)

if __name__ == "__main__":
    make_kepler_sc_cache()
