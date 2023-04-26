import numpy as np
from res_unit import ResUnit


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

    return revenue_loss


def riskToUtility(county: str, county_data: dict, samples, netMetering: bool):

    risk = np.empty(0)
    normResUnit = ResUnit(load_profile=county_data['countyLoadProfiles'][county],
                          ghi=county_data['countyGHI'][county],
                          pv_module_rating=county_data['PVModuleRating'],
                          es_module_rating=county_data['ESModuleRating'],
                          soc_min=county_data['socMin'],
                          peak_load=1,
                          retail_price=0.2231,
                          net_metering_price=0,
                          norm=True
                          )
    normResUnit.ESPowerLimit = 2
    if netMetering:
        normResUnit.netMeteringPrice = normResUnit.retailPrice / 2
    else:
        normResUnit.netMeteringPrice = 0
    projectedLoss = []

    for sample in samples:
        normResUnit.PVSize = sample[0]
        normResUnit.ESSize = sample[1]
        sampleLoss = RevenueLoss(1.2, demand_load=normResUnit.loadProfile,
                                 demand_net=normResUnit.netLoadNoFailures(),
                                 retail_electricity_price=normResUnit.retailPrice,
                                 net_metering_price=normResUnit.netMeteringPrice)

        projectedLoss.append(sampleLoss)

    avgProjectedLoss = sum(projectedLoss) / samples.shape[0]
    risk = avgProjectedLoss / (np.multiply(normResUnit.loadProfile, normResUnit.retailPrice).sum())

    return risk
