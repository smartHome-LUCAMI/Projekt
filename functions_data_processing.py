import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def set_default(hour_span, data_frame, attribute, graphing_interval):
    # A function that sets the default values of presence in the home, based on certain criteria and common sense
    """
    Parameters:
        hour_span -> the time interval whitin which there is high certainty that someone is home (list of tuples)
        data_frame -> a data frame
        attribute -> the name of the column where the values of the function will be placed (String)
        graphing_interval -> the interval for which a graph would be displayed (list)

    """

    data_frame[attribute] = 0.1

    for interval in hour_span:
        mask = (data_frame.index.hour >= interval[0]) & (
            data_frame.index.hour <= interval[1]
        )
        data_frame[attribute].mask(cond=mask, other=0.9, inplace=True)

    star_index_date = data_frame.index.get_loc(graphing_interval[0])
    end_index_date = data_frame.index.get_loc(graphing_interval[1])

    sns.lineplot(
        x=data_frame.index[star_index_date:end_index_date],
        y=attribute,
        data=data_frame[star_index_date:end_index_date],
    )


def set_GT(hour_span, data_frame, attribute, graphing_interval):
    # A function that sets the Ground Truth values of presence in the home, based on certain criteria and common sense
    """
    Parameters:
        hour_span -> the time interval whitin which there is high certainty that someone is home (list of tuples)
        data_frame -> a data frame
        attribute -> the name of the column where the values of the function will be placed (String)
        graphing_interval -> the interval for which a graph would be displayed (list)

    """

    data_frame[attribute] = 0.1

    for interval in hour_span:
        mask = (data_frame.index.hour >= interval[0]) & (
            data_frame.index.hour <= interval[1]
        )
        data_frame[attribute].mask(cond=mask, other=0.9, inplace=True)

    star_index_date = data_frame.index.get_loc(graphing_interval[0])
    end_index_date = data_frame.index.get_loc(graphing_interval[1])

    sns.lineplot(
        x=data_frame.index[star_index_date:end_index_date],
        y="Ground Truth",
        data=data_frame[star_index_date:end_index_date],
    )


def tresholding(data_frame, attribute, treshold, graphing_interval):
    # A function that performs tresholding on the data on the given attribute
    """
    Parameters:

        data_frame -> a data frame
        attribute -> the name of the column where the values of the function will be placed (String)
        treshold -> the treshold point for which smaller values would get a value of 0.1 and larger a value of 0.9(int)
        graphing_interval -> the interval for which a graph would be displayed (list)

    """

    data_frame[attribute].mask(
        cond=(data_frame[attribute] >= treshold), inplace=True, other=0.9
    )
    data_frame[attribute].mask(
        cond=(data_frame[attribute] <= treshold), inplace=True, other=0.1
    )

    star_index_date = data_frame.index.get_loc(graphing_interval[0])
    end_index_date = data_frame.index.get_loc(graphing_interval[1])

    sns.lineplot(
        x=data_frame.index[star_index_date:end_index_date],
        y=attribute,
        data=data_frame[star_index_date:end_index_date],
    )


def pre_process(data_frame, attribute_1, attribute_2, attribute_3, graphing_interval):
    # rename - > vizualization
    data_frame[attribute_3] = data_frame[attribute_2]
    mask = data_frame[attribute_1] > data_frame[attribute_2]
    data_frame[attribute_3].mask(cond=mask, inplace=True, other=data_frame[attribute_1])

    star_index_date = data_frame.index.get_loc(graphing_interval[0])
    end_index_date = data_frame.index.get_loc(graphing_interval[1])

    sns.lineplot(
        x=data_frame.index[star_index_date:end_index_date],
        y=attribute_3,
        data=data_frame[star_index_date:end_index_date],
    )


def post_process(data_frame, attribute, time_span, treshold_interval):
    # A function that changes the value of the attribute if the are two values of logical 1 (0.9 in this case )in an interval smaller than the treshold interval
    """
    Parameters:

        data_frame -> a data frame
        attribute -> the name of the column where the values of the function will be placed (String)
        time_span -> the interval for which the function will be perfomred and displayed (list)
        treshold_interval -> an interval given in minutes for which the value of the attribute is changed accordingly

    """

    for i in pd.date_range(time_span[0], time_span[1], freq="19min"):
        for j in pd.date_range(
            start=i, end=i + pd.Timedelta(treshold_interval, "m"), freq="min"
        ):
            if (data_frame.loc[i, attribute] == 0.9) & (
                data_frame.loc[j, attribute] == 0.9
            ):
                data_frame.loc[i:j, attribute] = 0.9

    star_index_date = data_frame.index.get_loc(time_span[0])
    end_index_date = data_frame.index.get_loc(time_span[1])

    sns.lineplot(
        x=data_frame.index[star_index_date:end_index_date],
        y=attribute,
        data=data_frame[star_index_date:end_index_date],
    )
