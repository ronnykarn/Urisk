# script to create test distributions for LA County
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats

PVOptNorm = 4.2
ESOptNorm = 5.2

noOfCustomers = 1000
penetrationPercentage = 80
noOfCustomersWithoutDER = int(noOfCustomers * (1 - penetrationPercentage / 100))
arrayWithoutDER = np.zeros((noOfCustomersWithoutDER, 2))

# number of cus around peak
cusAroundPeak = int((penetrationPercentage * 50 / 100) * noOfCustomers / 100)
# create an array of size cus Around peak with peak values
arrayAroundPeak = np.tile([1, 1], [cusAroundPeak, 1])
# add noise to disperse data
arrayAroundPeak = arrayAroundPeak + np.random.normal(0, 0.25, (cusAroundPeak, 2))

customersWithHalfSize = int((penetrationPercentage * 10 / 100) * noOfCustomers / 100)
arrayWithHalfSize = np.tile([2.1, 2.65], [customersWithHalfSize, 1])
arrayWithHalfSize = arrayWithHalfSize + np.random.normal(0, 0.5, (customersWithHalfSize, 2))

customersWithTFSize = int((penetrationPercentage * 10 / 100) * noOfCustomers / 100)
arrayWithTFSize = np.tile([3.15, 3.9], [customersWithTFSize, 1])
arrayWithTFSize = arrayWithTFSize + np.random.normal(0, 0.25, (customersWithTFSize, 2))

customersWithPVOnly = int((penetrationPercentage * 30 / 100) * noOfCustomers / 100)
arrayWithPVOnly = np.tile([1.5, 0], [customersWithPVOnly, 1])
arrayWithPVOnly[:, 0] += np.random.normal(0, 0.5, customersWithPVOnly)

allCustomers = np.concatenate((arrayWithoutDER, arrayAroundPeak, arrayWithHalfSize,
                               arrayWithTFSize, arrayWithPVOnly), axis=0)
allCustomers[allCustomers < 0] = 0

customerData = pd.DataFrame(allCustomers, columns=['PVnorm', 'ESnorm'])
k = sns.jointplot(customerData, x='PVnorm', y='ESnorm')
fig, ax = plt.subplot(1, 1)
ax.hist()

cov = customerData.cov()
k = 1
