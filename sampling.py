import numpy as np
import scipy as sp
from scipy import stats


def generateCorrUniSamples(sample_size, covariance):
    samplesUniform = np.random.uniform(0, 1, (sample_size, covariance.shape[0]))

    # correlate samples
    # convert uniform lhs samples to normal samples using ppf function
    uniToNorm = stats.norm.ppf(samplesUniform)

    # introduce correlation into the samples using Cholesky decomposition
    c = sp.linalg.cholesky(covariance, lower=True)
    correlatedNormSamples = np.dot(c, uniToNorm.transpose())
    correlatedNormSamples = correlatedNormSamples.transpose()

    # convert any nan values to -inf, nan values arise when there are zeros in the LHS sampler
    correlatedNormSamples[np.isnan(correlatedNormSamples)] = -np.inf

    # convert correlated normal samples to quantiles using inverse transformation
    quantiles = stats.norm.cdf(correlatedNormSamples)

    # quantiles are the correlated uniform samples in the sample space from [0, 1] transform these
    # samples using inverse transform and the truncated marginals

    return quantiles
