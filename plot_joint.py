import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from helperfuncs import *
from sampling import generateCorrUniSamples
from scipy import stats
import numpy as np
import os

plt.rc('font', size=16)
# Set the axes title font size
plt.rc('axes', titlesize=16)
# Set the axes labels font size
plt.rc('axes', labelsize=16)
# Set the font size for x tick labels
plt.rc('xtick', labelsize=10)
# Set the font size for y tick labels
plt.rc('ytick', labelsize=10)
# Set the legend font size
plt.rc('legend', fontsize=18)
# Set the font size of the figure title
plt.rc('figure', titlesize=16)


PVClip = 3
ESClip = 3
PVLoc = 0
ESLoc = 0
covariance = np.array([[1.579, 1.708], [1.708, 2.25]])
colors = ['r', 'b', 'g', 'k']

laResults = pd.read_csv('results\\datafiles\\risk_scale_la.csv')
sampleSize = 100
for step in range(1, 5):
    scale = 0.25 * step
    PVLims = getClips(PVLoc, scale, 0, PVClip)
    ESLims = getClips(ESLoc, scale, 0, ESClip)

    corrUniSamples = generateCorrUniSamples(sampleSize, covariance)

    # Convert the correlated uniform samples to the PVnorm and ESnorm space using inverse integral transform and
    # with the marginals of PV norm and ES norm
    PVSample = stats.truncnorm.ppf(corrUniSamples[:, 0], PVLims['a'], PVLims['b'], loc=PVLoc, scale=scale)
    ESSample = stats.truncnorm.ppf(corrUniSamples[:, 1], ESLims['a'], ESLims['b'], loc=ESLoc, scale=scale)

    # scaleArray = np.ones(sampleSize) * scale

    jointSample = np.vstack((PVSample, ESSample)).T
    jointSampleDf = pd.DataFrame(jointSample, columns=['PVnorm', 'ESnorm'])

    if step == 1:
        dependencePlot = sns.jointplot(data=jointSampleDf, x='PVnorm', y='ESnorm', color=colors[step-1],
                                       kind='kde')
        dependencePlot.fig.suptitle('Joint distribution (PVnorm, ESnorm) at scale = '+str(scale))
        figName = 'joint_distribution_'+str(scale)+'.png'
        dependencePlot.savefig(os.path.join('results\\plots', figName), bbox_inches='tight', dpi=300)
    else:
        pass

    risk = laResults[laResults['scale'] == scale]['risk'].values[0]
    riskNM = laResults[laResults['scale'] == scale]['riskNM'].values[0]

    x = sns.jointplot(data=jointSampleDf, x='PVnorm', y='ESnorm', color=colors[step-1],
                      marginal_kws=dict(bins=20, fill=False))
    x.fig.suptitle('Risk at scale = '+str(scale))
    x.ax_joint.text(0, jointSampleDf['ESnorm'].quantile(0.99),
                    'Risk with NM = '+str("{:.3f}".format(riskNM))+'\n Risk = '+str("{:.3f}".format(risk)),
                    bbox=dict(boxstyle='square', pad=0.3, edgecolor='orange', facecolor='yellow'))
    figName = 'laCounty_'+str(scale)+'.png'
    x.savefig(os.path.join('results\\plots', figName), bbox_inches='tight', dpi=300)


k=1


