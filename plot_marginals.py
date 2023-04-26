# script to create a practical distribution for the LA County

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from helperfuncs import *

# distribution centered at PVnorm = 0 and ESnorm = 0 and at different scales
PVClip = 3
ESClip = 3
PVLoc = 0
ESLoc = 0

colours = ['r', 'g', 'b', 'k']
figPdf, axPdf = plt.subplots()
figCdf, axCdf = plt.subplots()
for step in range(1, 5):
    scale = 0.25 * step
    lims = getClips(PVLoc, scale, 0, PVClip)
    # plot distribution
    s = np.linspace(stats.truncnorm.ppf(0.01, lims['a'], lims['b'], loc=PVLoc, scale=scale),
                    stats.truncnorm.ppf(0.99, lims['a'], lims['b'], loc=PVLoc, scale=scale), 100)
    rv = stats.truncnorm(lims['a'], lims['b'], loc=0, scale=scale)
    axPdf.plot(s, rv.pdf(s), colours[step - 1] + '-', lw=2, label='scale = ' + str(scale))
    axCdf.plot(s, rv.cdf(s), colours[step - 1] + '-', lw=2, label='scale = ' + str(scale))
    axPdf.legend()
    axCdf.legend()
figPdf.suptitle('Probability distributions for Varying penetration in PV')
axPdf.set_xlabel('PVnorm')
axPdf.set_ylabel('Density')
figPdf.savefig('results\\plots\\pdf_zeroloc.png', bbox_inches='tight', dpi=300)
figCdf.suptitle('cumulative distributions for Varying penetration in PV')
axCdf.set_xlabel('PVnorm')
axCdf.set_ylabel('Probability')
figCdf.savefig('results\\plots\\cdf_zeroloc.png', bbox_inches='tight', dpi=300)


