import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

data = pd.read_csv('2022_APMCM_C_Data.csv',encoding='gb18030')
data.head(10)

data['dt'] = pd.to_datetime(data['dt'])
data.index = data['dt']
data['Year'] = data['dt'].dt.year
data_2010 = data[data['Year']==2010][['AverageTemperature','City','Latitude','Longitude']]

def clear_Latitude(s):
    if 'N' in s:
        return float(s.replace('N',''))
    else:
        return -float(s.replace('S',''))
def clear_Longitude(s):
    if 'E' in s:
        return float(s.replace('E',''))
    else:
        return -float(s.replace('W',''))
data_2010['Latitude'] = data_2010['Latitude'].apply(clear_Latitude)
data_2010['Longitude'] = data_2010['Longitude'].apply(clear_Longitude)

city_data_df = data_2010.groupby('City').mean()

f, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
df = city_data_df
shifted_cols = df.columns
corrmat = df[shifted_cols].corr()

sns.heatmap(corrmat, annot=True, vmin=-1, vmax=1, cmap='coolwarm_r')
ax.set_title('position correlation', fontsize=16)
plt.tight_layout()
plt.savefig('fig/position correlation.png',dpi=300, bbox_inches = 'tight')
plt.show()

Y= city_data_df['AverageTemperature']
X1 = city_data_df.drop(columns=['AverageTemperature'])
X= sm.add_constant(X1)
result = sm.OLS(Y,X).fit()
result.summary()
print(result.summary())

China_data = pd.read_csv('clear_China_city_AvgTemperature.csv')
China_data.head(10)
China_data.index =pd.to_datetime(China_data['date'])
Shanghai_data = China_data[China_data['City'] == 'Shanghai']
Shanghai_data['AverageTemperature'][Shanghai_data['AverageTemperature']<-18]=np.nan

Shanghai_data = Shanghai_data.fillna(method = 'ffill',axis=0)
Shanghai_data.AverageTemperature.plot(figsize=(20, 5))
plt.xlabel('Average Temperature')
plt.title('Average Temperature in Shanghai')
plt.savefig('fig/Shanghai historical temperature .png',dpi=300, bbox_inches = 'tight')
plt.show()

decomposition = seasonal_decompose(Shanghai_data['AverageTemperature'], model='additive', period=365, extrapolate_trend='freq')
fig, axs = plt.subplots(4, figsize=(12, 6))
fig.suptitle('Time series decomposition')
decomposition.observed.plot(ax=axs[0])
decomposition.trend.plot(ax=axs[1])
decomposition.seasonal.plot(ax=axs[2])
decomposition.resid.plot(ax=axs[3])
axs[0].set_ylabel('Observed')
axs[1].set_ylabel('Trend')
axs[2].set_ylabel('Seasonal')
axs[3].set_ylabel('Residual')
plt.subplots_adjust( hspace=1 )
plt.savefig('fig/seasonal.png',dpi=300, bbox_inches = 'tight')

adf_test = adfuller(decomposition.resid)
print(f"p-value = {adf_test[1]}")