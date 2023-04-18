import pandas as pd
import numpy as np
from res_unit import ResUnit


def main():
    """
    Application entry point
    """

    # read data
    counties_profiles = pd.read_csv('datafiles\\load_profiles.csv')
    counties_ghi = pd.read_csv('datafiles\\ghi_counties.csv') / 1000

    testCounty = 'Los Angeles County'
    peak_loads = [2, 3, 4, 5]
    residential_units = {'unit_' + str(x): ResUnit(load_profile=counties_profiles[testCounty],
                                                   ghi=counties_ghi[testCounty],
                                                   pv_module_rating=0.3,
                                                   es_module_rating=2,
                                                   soc_min=0.1,
                                                   peak_load=x,
                                                   retail_price=0.213,
                                                   net_metering_price=0.04) for x in peak_loads}

    risk = {}

    for key, value in residential_units.items():
        value.optSizing(time_horizon=8760)
        unit_data = []
        for size in range(1, 4):
            PVSizingFactor = size * 0.25
            ESSizingFactor = size * 0.25
            value.netLoadNoFailures(PVSizingFactor, ESSizingFactor)
            unit_data.append(value.riskToUtility())
        risk[key] = unit_data

    k = 1


if __name__ == '__main__':
    main()
