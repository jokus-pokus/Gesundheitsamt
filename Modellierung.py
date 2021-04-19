import pandas as pd
from matplotlib import pyplot as plt
from fbprophet import Prophet
from DatenSammlung import DatenVergangenheitHolen, FeiertageHolen, WetterVorhersageNBG
from DatenVerarbeitung import DatenVerarbeitung

from datetime import date

today = date.today()

df = DatenVerarbeitung()
<<<<<<< HEAD
=======

>>>>>>> 0e40d95597946761b07f5f8a6b1cbcdffaffb23a
WetterVorhersage = WetterVorhersageNBG()

df_test = df

trainings_zeitraum_von = '2020-8-01'
df_test = df_test.loc[df_test.index>trainings_zeitraum_von].copy()

df_test= df_test.rename(columns={"7TIW": "y"})
df_test = df_test.reset_index()
df_test= df_test.rename(columns={"Date": "ds"})

m = Prophet(changepoint_prior_scale=2)
m.add_country_holidays(country_name='DE')
m.add_regressor('Temperatur')
m.add_regressor('ResNbg')
m.fit(df_test)

future = m.make_future_dataframe(periods=10,include_history=False)
future = future.set_index('ds')

future['Temperatur'] = future.join(WetterVorhersage)
<<<<<<< HEAD
future['ResNbg'] = df_test.ResNbg.iloc[-1]
=======
future['ResNbg'] = 75
>>>>>>> 0e40d95597946761b07f5f8a6b1cbcdffaffb23a
future = future.reset_index()

forecast = m.predict(future)

fig = m.plot(forecast)
ax = fig.gca()
ax.set_title(today, size=34)
<<<<<<< HEAD
plt.tight_layout()
=======
>>>>>>> 0e40d95597946761b07f5f8a6b1cbcdffaffb23a
fig.savefig('Vorhersagen/'+str(today)+'.png')

