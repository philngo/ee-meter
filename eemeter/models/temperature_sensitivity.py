import scipy.optimize as opt
import numpy as np

class ModelBase(object):
    def __init__(self,x0,bounds):
        self.x0 = x0
        self.bounds = bounds

    def parameter_optimization(self,average_daily_usages,observed_daily_temps):
        def objective_function(params):
            usages_est = self.compute_usage_estimates(params,observed_daily_temps)
            return np.sum((average_daily_usages - usages_est)**2)

        assert len(average_daily_usages) == len(observed_daily_temps)

        result = opt.minimize(objective_function,x0=self.x0,bounds=self.bounds)
        params = result.x
        return params

class DoubleBalancePointModel(ModelBase):

    @staticmethod
    def compute_usage_estimates(params,observed_daily_temps):
        # get parameters
        ts_low,ts_high,base_load,bp_low,bp_diff = params
        bp_high = bp_low + bp_diff

        hdds = []
        cdds = []
        for interval_daily_temps in observed_daily_temps:
            hdd = 0
            cdd = 0
            for daily_temp in interval_daily_temps:
                if not np.isnan(daily_temp):
                    if daily_temp <= bp_low:
                        hdd += bp_low - daily_temp
                    elif daily_temp >= bp_high:
                        cdd += daily_temp - bp_high
            hdds.append(hdd)
            cdds.append(cdd)

        estimates = []
        for hdd,cdd in zip(hdds,cdds):
            estimate = base_load + ts_low*hdd + ts_high*cdd
            estimates.append(estimate)

        return np.array(estimates)

class PRISMModel(ModelBase):

    @staticmethod
    def compute_usage_estimates(params,observed_daily_temps):
        # get parameters
        reference_temperature,base_level_consumption,heating_slope = params

        hdds = []
        for interval_daily_temps in observed_daily_temps:
            hdd = 0
            for daily_temp in interval_daily_temps:
                if not np.isnan(daily_temp):
                    if daily_temp <= reference_temperature:
                        hdd += reference_temperature - daily_temp
            hdds.append(hdd)

        estimates = [base_level_consumption + heating_slope*hdd for hdd in hdds]

        return np.array(estimates)
