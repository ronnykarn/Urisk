import numpy as np
import pandas as pd
from scipy import stats

from helperfuncs import *
from import_data import import_data
from risk import *
from sampling import generateCorrUniSamples
import random as r

r.seed(1234567)

data = import_data()
covariance = np.array([[1.579, 1.708], [1.708, 2.25]])
PVClip = 3
ESClip = 3
PVLoc = 0
ESLoc = 0

riskDf = pd.DataFrame(
    columns=['scale', 'riskNM']
)

for step in range(1, 5):
    scale = 0.25 * step
    PVLims = getClips(PVLoc, scale, 0, PVClip)
    ESLims = getClips(ESLoc, scale, 0, ESClip)

    convergenceCriteria = 1
    riskPerIteration = np.empty(0)
    riskPerIterationNM = np.empty(0)
    sampleCounter = 0

    while convergenceCriteria > 0.05:
        samples = 2
        sampleCounter = sampleCounter + samples

        riskPerSample = np.zeros(samples)
        riskPerSampleNM = np.zeros(samples)

        for i in range(samples):
            # Draw correlated Uniform samples correlated by the covariance matrix
            corrUniSamples = generateCorrUniSamples(20, covariance)

            # Convert the correlated uniform samples to the PVnorm and ESnorm space using inverse integral transform and
            # with the marginals of PV norm and ES norm
            PVSample = stats.truncnorm.ppf(corrUniSamples[:, 0], PVLims['a'], PVLims['b'], loc=PVLoc, scale=scale)
            ESSample = stats.truncnorm.ppf(corrUniSamples[:, 1], ESLims['a'], ESLims['b'], loc=ESLoc, scale=scale)

            jointSample = np.vstack((PVSample, ESSample)).T

            riskPerSample[i] = riskToUtility('Los Angeles County', data, jointSample, netMetering=False)
            riskPerSampleNM[i] = riskToUtility('Los Angeles County', data, jointSample, netMetering=True)

        riskPerIteration = np.append(riskPerIteration, riskPerSample)
        riskPerIterationNM = np.append(riskPerIterationNM, riskPerSampleNM)
        cov = np.sqrt(np.var(riskPerIteration) / sampleCounter) / np.mean(riskPerIteration)
        covNM = np.sqrt(np.var(riskPerIterationNM) / sampleCounter) / np.mean(riskPerIterationNM)

        convergenceCriteria = max(cov, covNM)

    to_append = pd.DataFrame([{
        'scale': scale,
        'risk': riskPerIteration.mean(),
        'riskNM': riskPerIterationNM.mean()
    }])

    riskDf = pd.concat([riskDf, to_append])

riskDf.to_csv('results\\datafiles\\risk_scale_la.csv', index=False)

k = 1
