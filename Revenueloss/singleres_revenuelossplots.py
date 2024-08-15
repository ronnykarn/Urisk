# Script to plot the results from the simulation

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the default text font size
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
plt.rc('figure', titlesize=20)

# import results
LAdata = pd.read_csv('results\\datafiles\\revenue_loss_la.csv')

LANNM = LAdata[LAdata['Net_metering'] == '0 * retail price']
LAQuartNM = LAdata[LAdata['Net_metering'] == '0.25 * retail price']
LAHalfNM = LAdata[LAdata['Net_metering'] == '0.5 * retail price']


dfHeatmap = LANNM.pivot(index='ES(kWh)', columns='PV(kW)', values='Revenue_pct_change')
dfHeatmap = dfHeatmap.iloc[::-1]
dfHeatmapQuartNM = LAQuartNM.pivot(index='ES(kWh)', columns='PV(kW)', values='Revenue_pct_change')
dfHeatmapQuartNM = dfHeatmapQuartNM.iloc[::-1]
dfHeatmapHalfNM = LAHalfNM.pivot(index='ES(kWh)', columns='PV(kW)', values='Revenue_pct_change')
dfHeatmapHalfNM = dfHeatmapHalfNM.iloc[::-1]


vMin = min(dfHeatmap.values.min(), dfHeatmapHalfNM.values.min())
vMax = max(dfHeatmap.values.max(), dfHeatmapHalfNM.values.max())

fig = plt.figure(figsize=(10, 6))
gs = fig.add_gridspec(1, 4, width_ratios=[4, 4, 4, 0.25])
(ax1, ax2, ax3, ax4) = gs.subplots()

sns.heatmap(dfHeatmap, cmap='autumn', vmin=vMin, vmax=vMax, square=True, linewidth=0.5, linecolor='black', ax=ax1,
            cbar=None)
ax1.set_title('NMP = 0')

sns.heatmap(dfHeatmapQuartNM, cmap='autumn', vmin=vMin, vmax=vMax, square=True, linewidths=0.5, yticklabels=False,
            linecolor='black', cbar=None, ax=ax2)
ax2.set_ylabel('')
ax2.set_title('NMP = 0.25*REP')

sns.heatmap(dfHeatmapHalfNM, cmap='autumn', vmin=vMin, vmax=vMax, square=True, linewidths=0.5, yticklabels=False,
            linecolor='black', cbar=None, ax=ax3)
ax3.set_ylabel('')
ax3.set_title('NMP = 0.5*REP')

fig.colorbar(ax3.collections[0], cax=ax4)
ax4.set_ylabel('Percentage change in Revenue')

fig.figure.savefig("results\\plots_v0\\revenue_loss_la.png", bbox_inches='tight', dpi=500)

k=1


