from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
import numpy as np
import pandas as pd
from itertools import product
import warnings

warnings.filterwarnings('ignore')

data = pd.read_csv('land month std data.csv')
plt.figure(figsize=[16, 9])  # Set dimensions for figure
# plt.plot(data['Year,'], data['Anomaly,'])

# dt=data["std data"]

plt.plot(data['std data'])
plt.title('Temperature')
plt.ylabel('Temperature')
plt.xlabel('Date')
# plt.xticks(rotation=90)
# plt.grid(True)
plt.show()

plot_pacf(data['std data'])
plot_acf(data['std data'])
plt.show()

ad_fuller_result = adfuller(data['std data'])
print(f'ADF Statistic: {ad_fuller_result[0]}')
print(f'p-value: {ad_fuller_result[1]}')

plt.figure(figsize=[16, 9]);  # Set dimensions for figure
plt.plot(data['std data'])
plt.title("Log Difference of Quarterly EPS for Johnson & Johnson")
plt.show()

data['std data'] = data['std data'].diff(12)
data = data.drop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], axis=0).reset_index(drop=True)
plt.figure(figsize=[16, 9]);  # Set dimensions for figure
plt.plot(data['std data'])
plt.title("Log Difference of Quarterly EPS for Johnson & Johnson")
plt.show()

data['std data'][0] = 0
print(data)
ad_fuller_result = adfuller(data['std data'])
print(f'ADF Statistic: {ad_fuller_result[0]}')
print(f'p-value: {ad_fuller_result[1]}')

plot_pacf(data['std data']);
plot_acf(data['std data']);


def optimize_SARIMA(parameters_list, d, D, s, exog):
    """
        Return dataframe with parameters, corresponding AIC and SSE

        parameters_list - list with (p, q, P, Q) tuples
        d - integration order
        D - seasonal integration order
        s - length of season
        exog - the exogenous variable
    """

    results = []

    for param in tqdm_notebook(parameters_list):
        try:
            model = SARIMAX(exog, order=(param[0], d, param[1]), seasonal_order=(param[2], D, param[3], s)).fit(disp=-1)
        except:
            continue

        aic = model.aic
        results.append([param, aic])

    result_df = pd.DataFrame(results)
    result_df.columns = ['(p,q)x(P,Q)', 'AIC']
    # Sort in ascending order, lower AIC is better
    result_df = result_df.sort_values(by='AIC', ascending=True).reset_index(drop=True)

    return result_df


a=4
# p = range(0, 12, 1)
# d = 1
# q = range(0, 12, 1)
p = range(0, a, 1)
d = 1
q = range(0, a, 1)

# P = range(0, a, 1)
# D = 1
# Q = range(0, 12, 1)
P = range(0, a, 1)
D = 1
Q = range(0, a, 1)

s = 12
parameters = product(p, q, P, Q)
parameters_list = list(parameters)
print(len(parameters_list))

result_df = optimize_SARIMA(parameters_list, 1, 1, s, data['std data'])
print(result_df)
