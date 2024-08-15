# evaluate the revenue lost by the utility in the presence of BTM DER

import pandas as pd
from import_data import import_data
from res_unit import ResUnit
from risk import RevenueLoss
import random as r

r.seed(227)

# import data into a dictionary
data = import_data()

# simulation for LA county
testCounty = 'Los Angeles County'
peakLoad = 4.5

revenueLoss = pd.DataFrame(
    columns=['county', 'PV(kW)', 'ES(kWh)', 'Revenue_loss', 'Actual_revenue',
             'Revenue_pct_change', 'Net_metering']
)

for netMeteringstate in [0, 1/4, 1/2]:
    laResUnit = ResUnit(load_profile=data['countyLoadProfiles'][testCounty],
                        ghi=data['countyGHI'][testCounty],
                        pv_module_rating=data['PVModuleRating'],
                        es_module_rating=data['ESModuleRating'],
                        soc_min=data['socMin'],
                        peak_load=peakLoad,
                        retail_price=0.2231,
                        net_metering_price=0,
                        norm=False)
    laResUnit.ESPowerLimit = 2 * peakLoad

    if netMeteringstate == 0:
        laResUnit.netMeteringPrice = 0
    elif netMeteringstate == 1 / 2:
        laResUnit.netMeteringPrice = laResUnit.retailPrice / 2
    elif netMeteringstate == 1 / 4:
        laResUnit.netMeteringPrice = laResUnit.retailPrice / 4

    PVMax = 10.5
    PVStep = 1.5
    ESMax = 20
    ESStep = 2

    for stepPV in range(int(PVMax / PVStep)):
        PVSize = (stepPV + 1) * PVStep
        for stepES in range(int(ESMax / ESStep)):
            ESSize = (stepES + 1) * ESStep

            # set PV and ES sizes and calculate net load
            laResUnit.PVSize = PVSize
            laResUnit.ESSize = ESSize
            laResUnit.netLoadNoFailures()

            # evaluate the lost revenue
            lostRevenue = RevenueLoss(1.2, laResUnit.loadTimeSeries, laResUnit.netLoadNoFailures(),
                                      laResUnit.retailPrice, laResUnit.netMeteringPrice)
            revenueNoDER = (laResUnit.loadTimeSeries * laResUnit.retailPrice).sum()
            to_append = pd.DataFrame([{
                'county': testCounty,
                'PV(kW)': PVSize,
                'ES(kWh)': laResUnit.ESSize,
                'Revenue_loss': lostRevenue,
                'Actual_revenue': revenueNoDER,
                'Revenue_pct_change': (-lostRevenue) * 100 / revenueNoDER,
                'Net_metering': str(netMeteringstate) + ' * retail price'
            }])

            revenueLoss = pd.concat([revenueLoss, to_append])

revenueLoss.to_csv('results\\datafiles\\revenue_loss_la.csv', index=False)

k=1