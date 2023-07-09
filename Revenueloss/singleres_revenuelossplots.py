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
revenueLossLA = pd.read_csv('../results/datafiles/revenue_loss_la.csv')
revenueLossNMLA = pd.read_csv('../results/datafiles/revenue_loss_nm_la.csv')

dfHeatmap = revenueLossLA.pivot(index='ES(kWh)', columns='PV(kW)', values='Revenue_loss')
dfHeatmap = dfHeatmap.iloc[::-1]
dfHeatmapNM = revenueLossNMLA.pivot(index='ES(kWh)', columns='PV(kW)', values='Revenue_loss')
dfHeatmapNM = dfHeatmapNM.iloc[::-1]

vMin = min(dfHeatmap.values.min(), dfHeatmapNM.values.min())
vMax = max(dfHeatmap.values.max(), dfHeatmapNM.values.max())

fig = plt.figure(figsize=(10, 6))
fig.suptitle('Projected loss in Revenue - LA County')
gs = fig.add_gridspec(1, 3, width_ratios=[4, 4, 0.25])
(ax1, ax2, ax3) = gs.subplots()

sns.heatmap(dfHeatmap, cmap='Reds', vmin=vMin, vmax=vMax, square=True, linewidth=0.5, linecolor='black', ax=ax1,
            cbar=None)
ax1.set_title('Without Net Metering')
sns.heatmap(dfHeatmapNM, cmap='Reds', vmin=vMin, vmax=vMax, square=True, linewidths=0.5, yticklabels=False,
            linecolor='black', cbar=None, ax=ax2)
ax2.set_ylabel('')
ax2.set_title('With Net Metering')
fig.colorbar(ax1.collections[0], cax=ax3)
ax3.set_ylabel('Projected Loss($)')

fig.figure.savefig("results\\plots\\revenue_loss_la.png", bbox_inches='tight', dpi=500)


