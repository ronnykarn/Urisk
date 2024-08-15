# Code to evaluate risk metric with actual values vs normalized values. The normalization factor used will be the peak
# load of the residential unit.

import random as r
import pandas as pd
from res_unit import ResUnit

r.seed(10)

load_profiles = pd.read_csv('datafiles\\load_profiles.csv')
counties_ghi = pd.read_csv('datafiles\\ghi_counties.csv') / 1000

testCounty = 'Los Angeles County'
peakLoad = 4.5
RUActual = ResUnit(load_profile=load_profiles[testCounty],
                   ghi=counties_ghi[testCounty],
                   pv_module_rating=0.3,
                   es_module_rating=2,
                   soc_min=1,
                   peak_load=peakLoad,
                   retail_price=0.213,
                   net_metering_price=0.04, norm=False)
RUActual.PVSize = 17
RUActual.ESSize = 20
RUActual.ESPowerLimit = 2*peakLoad
RUActual.optSizing(time_horizon=8760)
RUActual.netLoadNoFailures()
indices_actual = RUActual.evalReliabilityGridConnected()
actual_risk = RUActual.riskToUtility()

RUNormalized = ResUnit(load_profile=load_profiles[testCounty],
                       ghi=counties_ghi[testCounty],
                       pv_module_rating=0.3,
                       es_module_rating=2,
                       soc_min=1,
                       peak_load=peakLoad,
                       retail_price=0.213,
                       net_metering_price=0.04, norm=True)
RUNormalized.PVSize = 17/peakLoad
RUNormalized.ESSize = 20/peakLoad
RUNormalized.ESPowerLimit = 2*peakLoad/peakLoad
RUNormalized.optSizing(time_horizon=8760)
RUNormalized.netLoadNoFailures()
indices_normalized = RUNormalized.evalReliabilityGridConnected()
normal_risk = RUNormalized.riskToUtility()

k=1
