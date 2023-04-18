import numpy as np


def RevenueLoss(defection_criteria, demand_load, demand_net, retail_electricity_price,
                net_metering_price):
    """
    Calculates the revenue loss

    :param defection_criteria:
    :param demand_load:
    :param demand_net:
    :param retail_electricity_price:
    :param net_metering_price:
    :return:
    """

    lossGridDefection = np.multiply(demand_load, retail_electricity_price).sum()
    lossGridSupplemented = 0
    for hour in range(8760):
        lossGridSupplemented += np.heaviside(demand_net[hour], 1) * (demand_load[hour]
                                                                     - demand_net[hour]) * retail_electricity_price \
                                + (1 - np.heaviside(demand_net[hour], 1)) * (demand_load[hour]
                                                                             * retail_electricity_price
                                                                             - demand_net[hour] * net_metering_price)
    revenue_loss = np.heaviside(1 - defection_criteria, 1) * lossGridDefection + np.heaviside(
        defection_criteria - 1, 1) * lossGridSupplemented
    k=1

    return revenue_loss
