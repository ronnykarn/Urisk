# evaluate the revenue lost by the utility in the presence of BTM DER for all counties

import pandas as pd
from import_data import import_data
from res_unit import ResUnit
from risk import RevenueLoss

# import data into a dictionary
data = import_data()

countiesData = data['countiesData']
revenueLoss = pd.DataFrame(
    columns=['county', 'climate_zone', 'PV(kW)', 'ES(kWh)', 'Revenue_loss', 'Actual_revenue',
             'Revenue_pct_change', 'Net_metering']
)

for netMetering in [True, False]:
    for county in countiesData['county']:
        locationData = countiesData[countiesData['county'] == county]
        peakLoad = locationData.iloc[0]['peak_load']
        residence = ResUnit(load_profile=data['countyLoadProfiles'][county],
                            ghi=data['countyGHI'][county],
                            pv_module_rating=data['PVModuleRating'],
                            es_module_rating=data['ESModuleRating'],
                            soc_min=data['socMin'],
                            peak_load=peakLoad,
                            retail_price=locationData.iloc[0]['avg_rep'],
                            net_metering_price=0,
                            norm=False)
        residence.ESPowerLimit = 2 * peakLoad

        if netMetering:
            residence.netMeteringPrice = residence.retailPrice / 2
        else:
            residence.netMeteringPrice = 0

        PVMax = 10.5
        PVStep = 1.5
        residence.ESSize = 2 * peakLoad

        for stepPV in range(int(PVMax / PVStep)):
            PVSize = (stepPV + 1) * PVStep

            # set PV and ES sizes and calculate net load
            residence.PVSize = PVSize
            residence.netLoadNoFailures()

            # evaluate lost revenue
            lostRevenue = RevenueLoss(1.2, residence.loadTimeSeries, residence.netLoadNoFailures(),
                                      residence.retailPrice, residence.netMeteringPrice)
            revenueNoDER = (residence.loadTimeSeries * residence.retailPrice).sum()
            to_append = pd.DataFrame([{
                'county': county,
                'climate_zone': locationData.iloc[0]['climate_zone'],
                'PV(kW)': PVSize,
                'ES(kWh)': residence.ESSize,
                'Revenue_loss': lostRevenue,
                'Actual_revenue': revenueNoDER,
                'Revenue_pct_change': (-lostRevenue) * 100 / revenueNoDER,
                'Net_metering': netMetering
            }])

            revenueLoss = pd.concat([revenueLoss, to_append])

revenueLoss.to_csv('results\\datafiles\\revenue_loss_all_counties.csv')

k = 1
