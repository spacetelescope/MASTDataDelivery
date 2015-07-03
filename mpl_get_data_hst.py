"""
.. module:: mpl_get_data_hst

   :synopsis: Returns a failure JSON as a temporary measure until HST is
   supported natively.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

from data_series import DataSeries

#--------------------
def mpl_get_data_hst(obsid):
    """
    Given an HST observation ID, returns a failure JSON in the expected format.

    :param obsid: The HST observation ID to retrieve the data from.

    :type obsid: str

    :returns: JSON -- A failure status for this observation ID.

    Error codes:
    0 = No error.
    1 = No data available (unsupported mission currently).
    """

    errcode = 1
    return_dataseries = DataSeries('hst', obsid, [], [], [], [], errcode)

    # Return the DataSeries object back to the calling module.
    return return_dataseries
#--------------------
