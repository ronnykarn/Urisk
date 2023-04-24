from pulp import *
from pdrm.bess_model import *
from pdrm.ceval_indices import *
from revenue_loss import RevenueLoss


class ResUnit:
    """
    A class to model a residential unit
    """

    def __init__(self, load_profile, peak_load, ghi, pv_module_rating, es_module_rating,
                 retail_price, net_metering_price, soc_min, norm: bool):

        self.loadProfile = load_profile
        self.peakLoad = peak_load
        self.ghi = ghi
        self.retailPrice = retail_price
        self.netMeteringPrice = net_metering_price
        self.socMin = soc_min
        if norm:
            self.PVModuleRating = pv_module_rating / peak_load
            self.ESModuleRating = es_module_rating / peak_load
            self.loadTimeSeries = load_profile
        else:
            self.loadTimeSeries = load_profile * peak_load
            self.PVModuleRating = pv_module_rating
            self.ESModuleRating = es_module_rating

        self.PVSize = None
        self.ESSize = None
        self.ESPowerLimit = None
        self.optESSize = None
        self.optPVSize = None

    def optSizing(self, time_horizon):

        # create dictionaries for load and output per module variables
        D = makeDict([range(1, time_horizon + 1)], self.loadTimeSeries)
        outputPerModule = makeDict([range(1, time_horizon + 1)], self.PVModuleRating * 0.8 * self.ghi)

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
            prob += self.socMin * self.ESModuleRating * B <= S[j] <= self.ESModuleRating * B

        # Battery initial condition
        prob += S[0] == S[time_horizon]

        # The problem data is written to an .lp file
        prob.writeLP("OptimalSizing.lp")

        # solve the problem
        prob.solve()

        print("Status:", LpStatus[prob.status])

        self.optPVSize = X.varValue * self.PVModuleRating
        self.optESSize = B.varValue * self.ESModuleRating

        return [self.optPVSize, self.optESSize]

    def netLoadNoFailures(self):
        soc = 1
        deratingFactor = 0.8
        PVOutputTimeSeries = self.PVSize * deratingFactor * self.ghi

        netLoad = np.zeros(8760)
        for hour in range(8760):
            netLoad[hour], soc = bess_operation(self.ESPowerLimit, soc, self.socMin, self.ESSize,
                                                self.loadTimeSeries[hour],
                                                PVOutputTimeSeries[hour])
        setattr(self, 'netLoad', netLoad)

        return netLoad

    def riskToUtility(self):

        defectionCriteria = 1.2  # define something greater than 1
        risk = RevenueLoss(defectionCriteria, self.loadTimeSeries, self.netLoadNoFailures(), self.retailPrice,
                           self.netMeteringPrice) / (np.multiply(self.loadTimeSeries, self.retailPrice).sum())
        return risk

    def evalReliabilityGridConnected(self):
        indices = customer_evaluation_grid_connected(cov_convergence=0.075,
                                                     load_point_repair_time=11.43,
                                                     load_point_failure_rate=0.305,
                                                     hourly_load=self.loadTimeSeries,
                                                     acm_module_rating=self.PVModuleRating,
                                                     acm_repair_rate=0.0964337280, acm_failure_rate=4.35133e-05,
                                                     ghi_hourly=self.ghi, bess_state_of_charge_min=self.socMin,
                                                     bess_repair_rate=0.1, bess_failure_rate=0.0000114155,
                                                     bess_capacity=self.ESSize, pv_capacity=self.PVSize,
                                                     bess_power_limit=self.ESPowerLimit)
        setattr(self, 'indices', indices)
        return indices
