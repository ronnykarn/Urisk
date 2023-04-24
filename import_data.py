# script to import data from csv files and assign them to a dictionary

import pandas as pd


def import_data():
    # data from csv files
    counties_data = pd.read_csv('datafiles\\counties_data.csv')
    load_profiles = pd.read_csv('datafiles\\load_profiles.csv')
    counties_ghi = pd.read_csv('datafiles\\ghi_counties.csv') / 1000
    parameter_data = pd.read_csv('datafiles\\parameter_data.csv')

    # panel data
    PVModuleRating = parameter_data.iloc[0]['acm_module_rating']  # in kW
    PVFailureRate = parameter_data.iloc[0]['acm_failure_rate']  # f/yr
    PVRepairRate = parameter_data.iloc[0]['acm_repair_rate']  #

    # bess data
    ESModuleRating = parameter_data.iloc[0]['bess_module_rating']  # in kW
    ESFailureRate = parameter_data.iloc[0]['bess_failure_rate']
    ESRepairRate = parameter_data.iloc[0]['bess_repair_rate']
    socMin = parameter_data.iloc[0]['bess_state_of_charge_min']

    # load point data
    LPFailureRate = parameter_data.iloc[0]['loadpoint_failure_rate']
    LPRepairTime = parameter_data.iloc[0]['loadpoint_repair_time']

    data = {'countiesData': counties_data,
            'countyLoadProfiles': load_profiles,
            'countyGHI': counties_ghi,
            'PVModuleRating': PVModuleRating,
            'PVFailureRate': PVFailureRate,
            'PVRepairTime': PVRepairRate,
            'ESModuleRating': ESModuleRating,
            'ESFailureRate': ESFailureRate,
            'ESRepairRate': ESRepairRate,
            'socMin': socMin,
            'LPFailureRate': LPFailureRate,
            'LPRepairTime': LPRepairTime
            }

    return data
