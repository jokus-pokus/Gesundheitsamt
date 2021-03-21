import pandas as pd
from DatenSammlung import DatenVergangenheitHolen, FeiertageHolen
from datetime import date, timedelta


today = date.today()
yesterday = today - timedelta(days = 1)
print("Today's date:", today)

def DatenVerarbeitung():

    CoronaWerte, Wetter, Restriktionen = DatenVergangenheitHolen()

    CoronaWerte.loc[:,'Date'] = pd.to_datetime(CoronaWerte['Refdatum'])
    CoronaWerte.Date = CoronaWerte.Date.dt.date
    CoronaWerte = CoronaWerte.drop(columns=['Refdatum'])
    CoronaWerte.loc[:,'Date'] = pd.to_datetime(CoronaWerte['Date'])
    Wetter.DATE = Wetter.DATE.dt.date
    Wetter = Wetter.drop(columns=['STATION_ID','PARAMETER_SET','PARAMETER','QUALITY'])
    Wetter.loc[:,'DATE'] = pd.to_datetime(Wetter['DATE'])
    Wetter = Wetter.rename(columns={"VALUE": "Temperatur"})
    Restriktionen.loc[:,'Date'] = pd.to_datetime(Restriktionen['Date'],format='%Y%m%d')
    Restriktionen = Restriktionen.rename(columns={"StringencyIndexForDisplay": "ResNbg"})


    CoronaWerte = CoronaWerte.set_index('Date')
    Wetter = Wetter.set_index('DATE')
    Restriktionen = Restriktionen.set_index('Date')

    CoronaWerte = CoronaWerte.loc['2020-04-02':yesterday,:]
    Wetter = Wetter.loc['2020-04-02':yesterday,:]
    Restriktionen = Restriktionen.loc['2020-04-02':yesterday,:]

    Restriktionen = Restriktionen.interpolate(method='linear')
    Wetter = Wetter.interpolate(method='linear')
    CoronaWerte = CoronaWerte.interpolate(method='linear')

    CoronaWerte = CoronaWerte.join([Wetter,Restriktionen])

    return CoronaWerte

df = DatenVerarbeitung()
