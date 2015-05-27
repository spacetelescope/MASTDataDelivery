
#--------------------

class DataSeries(object):
    """
    Defines a Data Series object, which contains the data (plot series) and 
    plot labels for those series.
    """
    
    def __init__(self, mission, obsid, plot_series, plot_labels, errcode):
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

        :param errcode: An integer used to signal if there was a problem reading
        in the data.

        :type errcode: int

        """
        self.mission = mission
        self.obsid = obsid
        self.plot_series = plot_series
        self.plot_labels = plot_labels
        self.errcode = errcode

#--------------------
