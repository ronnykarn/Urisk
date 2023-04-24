# script to optimally size PV and ES for all the counties with data available

import pandas as pd
from import_data import import_data
from res_unit import ResUnit

# import data into a dictionary
data = import_data()

countiesData = data['countiesData']
sized_locations = pd.DataFrame(
    columns=['county', 'climate_zone', 'PV(kW)', 'ES(kWh)']
)

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
    residence.optSizing(time_horizon=8760)
    to_append = pd.DataFrame([{
        'county': county,
        'climate_zone': locationData.iloc[0]['climate_zone'],
        'PV(kW)': residence.optPVSize,
        'ES(kWh)': residence.optESSize
    }])
    sized_locations = pd.concat([sized_locations, to_append])

sized_locations.to_csv('results\\datafiles\\countywise_sized.csv', index=False)

k=1
