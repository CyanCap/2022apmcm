# This file contains a detailed summary of the land-surface average
# % results produced by the Berkeley Averaging method.  Temperatures are
# % in Celsius and reported as anomalies relative to the Jan 1951-Dec 1980
# % average.  Uncertainties represent the 95% confidence interval for
# % statistical and spatial undersampling effects.
# %
# % The current dataset presented here is described as:
# %
# %   Estimated Global Land-Surface TAVG based on the Complete Berkeley Dataset
# %
# %
# % This analysis was run on 03-Nov-2022 08:13:55
# %
# % Results are based on 50498 time series
# %   with 21051207 data points
# %
# % Estimated Jan 1951-Dec 1980 absolute temperature (C): 8.60 +/- 0.05
# %
# % As Earth's land is not distributed symmetrically about the equator, there
# % exists a mean seasonality to the global land-average.
# %
# % Estimated Jan 1951-Dec 1980 monthly absolute temperature:
# %      Jan   Feb   Mar   Apr   May   Jun   Jul   Aug   Sep   Oct   Nov   Dec
# %      2.59  3.20  5.29  8.29 11.28 13.43 14.31 13.84 12.04  9.20  6.07  3.63
# % +/-  0.12  0.08  0.06  0.07  0.07  0.08  0.09  0.08  0.06  0.07  0.07  0.10
# %
# % For each month, we report the estimated land-surface average for that
# % month and its uncertainty.  We also report the corresponding values for
# % year, five-year, ten-year, and twenty-year moving averages CENTERED about
# % that month (rounding down if the center is in between months).  For example,
# % the annual average from January to December 1950 is reported at June 1950.

import csv
import pandas as pd
import xlrd
import xlwt
import openpyxl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import font_manager
import random

yr = range(1750, 2022);
mr = range(0, 10);

avg = [2.59, 3.20, 5.29, 8.29, 11.28, 13.43, 14.31, 13.84, 12.04, 9.20, 6.07, 3.63]

df = pd.read_excel('./land avg monthly.xlsx', sheet_name='avg monthly', usecols=[2])

h, w = df.shape

valm = np.zeros(h)

valmj = []

for i in range(1, h):
    valm[i - 1] = df.values[i]
    valm[i - 1] = valm[i - 1] + avg[(i - 1) % 12]

valy = []

for i in range(0, int(len(valm) / 12)):
    tmp = 0
    for j in range(0, 11):
        tmp = tmp + valm[i * 12 + j]
    valy.append(tmp / 12)

for i in range(3264, 3274):
    valmj.append(valm[i])

wb = xlwt.Workbook()
ws = wb.add_sheet('std month data')
ws.write(0, 0, 'std data')
for i in range(1, h-1):
    ws.write(i, 0, valm[i]);

wb.save('../land month std data.xls')

wb = xlwt.Workbook()
ws = wb.add_sheet('std year avg data')
ws.write(0, 0, 'std data')
for i in range(1, len(valy)):
    ws.write(i, 0, valy[i])

wb.save('../land year std data.xls')

# print(valmj)
# plt.figure(1)
# plt.title('Average monthly temperature in 2022')
# plt.xlabel('month')
# plt.ylabel('temperature')
# plt.plot(mr, valmj)
# plt.savefig("./fig/Average monthly temperature in 2022.jpg")
#
# plt.figure(2)
# plt.title('The annual average temperature')
# plt.xlabel('year')
# plt.ylabel('temperature')
# plt.plot(yr, valy)
# plt.savefig("./fig/The annual average temperature.jpg")
# plt.show()

# git remote set-url origin https://<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>@github.com/CyanCap/2022apmcm.git
