import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('ggplot')

results = pd.read_csv('../results/datafiles/revenue_loss_all_counties.csv')

for zone in results['climate_zone'].unique():
    zonePlot = plt.figure()
    zonePlot.tight_layout()
    zonePlotAx = zonePlot.subplots()

    data = results[results['climate_zone'] == zone]
    noOfCounties = data['county'].unique().size
    sns.boxplot(data=data, x='Revenue_pct_change', y='PV(kW)', orient='h',
                hue='Net_metering', palette='Set1', ax=zonePlotAx,
                dodge=True, boxprops=dict(linewidth=0.7),
                whiskerprops=dict(linestyle='--', linewidth=0.7),
                medianprops=dict(linestyle='-', linewidth=0.5),
                capprops=dict(linestyle='-', linewidth=0.5),
                flierprops=dict(marker='x', markerfacecolor='none', markersize=3, markeredgecolor='black')
                )
    zonePlotAx.invert_xaxis()
    zonePlotAx.invert_yaxis()
    zonePlotAx.text(0.1, 0.9, 'counties = '+str(noOfCounties), transform=zonePlotAx.transAxes,
                    bbox=dict(boxstyle='square', pad=0.3, edgecolor='orange', facecolor='yellow'))
    zonePlotAx.set_xlabel('Projected % change in ($) revenue')
    zonePlotAx.axvline(0, ls='--')
    zonePlot.suptitle(zone + ' zone comparison')
    figName = zone + '.png'
    zonePlot.savefig(os.path.join('../results/plots', figName), bbox_inches='tight', dpi=500)

