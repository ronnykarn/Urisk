import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('ggplot')

results = pd.read_csv('results\\datafiles\\revenue_loss_all_counties.csv')

for zone in results['climate_zone'].unique():
    zonePlot = plt.figure()
    zonePlot.tight_layout()
    zonePlotAx = zonePlot.subplots()

    sns.boxplot(data=results[results['climate_zone'] == zone], x='Revenue_pct_change', y='PV(kW)', orient='h',
                hue='Net_metering', palette='Set1', ax=zonePlotAx,
                dodge=True, boxprops=dict(linewidth=0.7),
                whiskerprops=dict(linestyle='--', linewidth=0.7),
                medianprops=dict(linestyle='-', linewidth=0.5),
                capprops=dict(linestyle='-', linewidth=0.5),
                flierprops=dict(marker='x', markerfacecolor='none', markersize=3, markeredgecolor='black')
                )
    zonePlotAx.invert_xaxis()
    zonePlotAx.invert_yaxis()
    zonePlotAx.set_xlabel('Projected % change in ($) revenue')
    zonePlotAx.axvline(0, ls='--')
    zonePlot.suptitle(zone + ' zone comparison')
    figName = zone + '.png'
    zonePlot.savefig(os.path.join('results\\plots', figName), bbox_inches='tight', dpi=500)

