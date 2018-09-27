"""
.. module:: data_series

   :synopsis: Defines the DataSeries class.

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

#--------------------
class DataSeries(object):
    """
    Defines a Data Series object, which contains the data (plot series) and
    plot labels for those series.
    """

    def __init__(self, mission, obsid, plot_series, plot_labels,
                 xunits, yunits, errcode, is_ancillary=None):
        """
        Create a DataSeries object.

        :param mission: The mission this DataSeries comes from.

        :type mission: str

        :param obsid: The observation ID this DataSeries comes from.

        :type obsid: str

        :param plot_series: A 1-D list containing one or more 1-D lists that
        contain the (x,y) pairs for the given series of data.

        :type plot_series: list

        :param plot_labels: A 1-D list containing the strings to use as plot
        labels for each of the series of data.

        :type plot_series: list

        :param xunits: A 1-D list containing the strings to use as x-axis unit
        labels for each of the series of data.

        :type xunits: list

        :param yunits: A 1-D list containing the strings to use as y-axis unit
        labels for each of the series of data.

        :type yunits: list

        :param errcode: An integer used to signal if there was a problem reading
        in the data.

        :type errcode: int

        :param is_ancillary: A 1-D list of ints that, if set, indicates the
        returned data should NOT be plotted by default.  If set to 0, then DO
        plot by default.

        :type is_ancillary: list
        """
        self.mission = mission
        self.obsid = obsid
        self.plot_series = plot_series
        self.plot_labels = plot_labels
        self.xunits = xunits
        self.yunits = yunits
        self.errcode = errcode
        if is_ancillary is not None:
            self.is_ancillary = is_ancillary
        #--------------------
