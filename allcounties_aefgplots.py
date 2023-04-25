import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')
resultsNM = pd.read_csv('results\\datafiles\\revenue_loss_nm_cwise.csv')
results = pd.read_csv('results\\datafiles\\revenue_loss_cwise.csv')
climateZoneHue = ['#63b0c0', '#6d7cbd', '#8cb533', '#f1a336', '#b35414']

cwiseNMPlot = plt.figure()
cwiseNMPlot.tight_layout()
cwiseNMAx = cwiseNMPlot.subplots()

sns.boxplot(data=resultsNM, y='Revenue_pct_change', x='PV(kW)', hue='climate_zone',
            hue_order=['Marine', 'Cold', 'Mixed Humid', 'Hot Humid', 'Hot Dry'],
            dodge=True, palette=sns.color_palette(climateZoneHue), ax=cwiseNMAx, boxprops=dict(linewidth=0.7),
            whiskerprops=dict(linestyle='--', linewidth=0.7),
            medianprops=dict(linestyle='-', linewidth=0.5),
            capprops=dict(linestyle='-', linewidth=0.5),
            flierprops=dict(marker='x', markerfacecolor='none', markersize=3, markeredgecolor='black')
            )
cwiseNMAx.set_ylabel('Projected % change in ($) revenue')
cwiseNMAx.axhline(0, ls='--')
cwiseNMAx.text(0.5, -5, "reference for system without DER")
cwiseNMPlot.suptitle('With Net metering')
cwiseNMPlot.savefig('results\\plots\\revenue_loss_cwise_nm.png', bbox_inches='tight', dpi=500)

cwisePlot = plt.figure()
cwisePlot.tight_layout()
cwiseAx = cwisePlot.subplots()

sns.boxplot(data=results, y='Revenue_pct_change', x='PV(kW)', hue='climate_zone',
            hue_order=['Marine', 'Cold', 'Mixed Humid', 'Hot Humid', 'Hot Dry'],
            dodge=True, palette=sns.color_palette(climateZoneHue), ax=cwiseAx, boxprops=dict(linewidth=0.7),
            whiskerprops=dict(linestyle='--', linewidth=0.7),
            medianprops=dict(linestyle='-', linewidth=0.5),
            capprops=dict(linestyle='-', linewidth=0.5),
            flierprops=dict(marker='x', markerfacecolor='none', markersize=3, markeredgecolor='black')
            )
cwiseAx.set_ylabel('Projected % change in ($) revenue')
cwiseAx.axhline(0, ls='--')
cwiseAx.text(0.5, -2.5, "reference for system without DER")
cwisePlot.suptitle('Without Net metering')
cwisePlot.savefig('results\\plots\\revenue_loss_cwise.png', bbox_inches='tight', dpi=500)
