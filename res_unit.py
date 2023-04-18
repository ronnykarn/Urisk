from pulp import *
import numpy as np
from pdrm.bess_model import *
from revenue_loss import RevenueLoss


class ResUnit:
    """
    A class to model a residential unit
    """

    def __init__(self, load_profile, peak_load, ghi, pv_module_rating, es_module_rating,
                 retail_price, net_metering_price, soc_min):
        self.optESSize = None
        self.optPVSize = None
        self.loadProfile = load_profile
        self.peakLoad = peak_load
        self.loadTimeSeries = load_profile * peak_load
        self.ghi = ghi
        self.pv_module_rating = pv_module_rating
        self.es_module_rating = es_module_rating
        self.retail_price = retail_price
        self.net_metering_price = net_metering_price
        self.soc_min = soc_min
        self.no_pv_modules = None
        self.no_battery_modules = None

    def optSizing(self, time_horizon):

        # create dictionaries for load and output per module variables
        D = makeDict([range(1, time_horizon + 1)], self.loadTimeSeries)
        outputPerModule = makeDict([range(1, time_horizon + 1)], self.pv_module_rating * 0.8 * self.ghi)

        # create a prob variable to contain the problem
        prob = LpProblem("OptimalSizing", LpMinimize)

        # Create decision variables
        X = LpVariable("NoOfPanels", 0, None, LpInteger)
        B = LpVariable("NoOfBatteries", 0, None, LpInteger)
        S = LpVariable.dicts("AccumulatedEnergyInBatt", range(0, time_horizon + 1), 0)
        Y = LpVariable.dicts("PvToBatt", range(1, time_horizon + 1), 0)
        U = LpVariable.dicts("UnmetDemand", range(1, time_horizon + 1), 0)

        # The objective function added to the 'prob'
        prob += 3 * X + 16 * B, "Minimize PV cap and Batt Cap"

        # Add constraints to 'prob'
        # Reliability criterion
        prob += lpSum(U) <= (0.01 * sum(D.values()))

        for i in range(1, time_horizon + 1):
            # Battery charging discharging operation
            prob += S[i] == S[i - 1] + Y[i] + U[i] - D[i]

            # Unmet energy always less than or equal to demand
            prob += U[i] <= D[i]

            # Amount of energy stored is less than the energy generated from PV at time step
            prob += Y[i] <= outputPerModule[i] * X

        for j in range(0, time_horizon + 1):
            prob += self.soc_min * self.es_module_rating * B <= S[j] <= self.es_module_rating * B

        # Battery initial condition
        prob += S[0] == S[time_horizon]

        # The problem data is written to an .lp file
        prob.writeLP("OptimalSizing.lp")

        # solve the problem
        prob.solve()

        print("Status:", LpStatus[prob.status])

        self.no_pv_modules = X.varValue
        self.no_battery_modules = B.varValue

        self.optPVSize = self.no_pv_modules * self.pv_module_rating
        self.optESSize = self.no_battery_modules * self.es_module_rating

        return self.optPVSize, self.optESSize

    def netLoadNoFailures(self, pv_sizing_factor, es_sizing_factor):
        soc = 1
        PVCapacity = self.optPVSize * pv_sizing_factor
        ESCapacity = self.optESSize * es_sizing_factor
        ESPowerLimit = 2 * self.peakLoad
        deratingFactor = 0.8
        PVOutputTimeSeries = PVCapacity * deratingFactor * self.ghi

        netLoad = np.zeros(8760)
        for hour in range(8760):
            netLoad[hour], soc = bess_operation(ESPowerLimit, soc, self.soc_min, ESCapacity, self.loadTimeSeries[hour],
                                                PVOutputTimeSeries[hour])
        setattr(self, 'netLoad', netLoad)

    def riskToUtility(self):

        defectionCriteria = 1.2  # define something greater than 1
        risk = RevenueLoss(defectionCriteria, self.loadTimeSeries, self.netLoad, self.retail_price,
                           self.net_metering_price)/(np.multiply(self.loadTimeSeries, self.retail_price).sum())
        return risk
