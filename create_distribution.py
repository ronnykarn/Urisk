# script to create test distributions for LA County

import pandas as pd
from import_data import import_data
from res_unit import ResUnit

# import data into a dictionary
data = import_data()

# simulation for LA county
optESSize = 0
optPVSize = 0
testCounty = 'Los Angeles County'
for peakLoad in range(101):
    testUnit = ResUnit(load_profile=data['countyLoadProfiles'][testCounty],
                       ghi=data['countyGHI'][testCounty],
                       pv_module_rating=data['PVModuleRating'],
                       es_module_rating=data['ESModuleRating'],
                       soc_min=data['socMin'],
                       peak_load=peakLoad,
                       retail_price=0.2231,
                       net_metering_price=0,
                       norm=True)
    testUnit.optSizing(time_horizon=8760)
    optESSize += testUnit.optESSize
    optPVSize += testUnit.optPVSize

avgOptESSize = optESSize/100
avgOptPVSize = optPVSize/100
k = 1
