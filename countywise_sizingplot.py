import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')

sizedLocations = pd.read_csv('results\\datafiles\\countywise_sized.csv')

# dropping outliers
dropIndex = sizedLocations[(sizedLocations['PV(kW)'] > 70) | (sizedLocations['ES(kWh)'] > 70)].index
sizedLocations.drop(dropIndex, inplace=True)

sizingPlot = plt.figure()
sizingPlot.tight_layout()
sizingAx = sizingPlot.subplots()
sns.scatterplot(data=sizedLocations, x='PV(kW)', y='ES(kWh)', hue='climate_zone', style='climate_zone',
                palette='Set1', ax=sizingAx, s=25)
sizingAx.set_ylabel('Energy storage capacity(kWh)')
sizingAx.set_xlabel('Rooftop PV capacity(kW)')
sizingPlot.suptitle('Optimal sizing of the DER')
sizingPlot.savefig('results\\plots\\sizing.png', bbox_inches='tight')
k = 1
