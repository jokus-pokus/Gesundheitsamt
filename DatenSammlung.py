import pandas as pd 
import glob
from datetime import date
from wetterdienst import Wetterdienst

import requests
import json
import numpy as np

today = date.today()
print("Today's date:", today)

def DatenVergangenheitHolen():

    # Daten des 7TIW holen
    download_dates = pd.date_range(start='20200402', end=today).strftime('%Y%m%d')

    base_url = ("https://www.lgl.bayern.de/gesundheit/infektionsschutz/infektionskrankheiten_a_z/coronavirus/karte_coronavirus/fallzahlen_archiv/")

    list_of_url = [base_url+date+str('_LK_coronazahlen.csv') for date in download_dates]

    df7TIW = pd.DataFrame()

    for url, date in zip(list_of_url,download_dates):
        try:
            tempdf7TIW = pd.read_csv(url, encoding='latin-1',delimiter=';',decimal=',')
            tempdf7TIW['Date'] = date
            df7TIW = pd.concat([df7TIW, tempdf7TIW])
        except:
            print(str('no data for ')+date)

    df7TIWnbg = df7TIW.loc[df7TIW['Regierungsbezirk Land-/Stadtkreis'] == 'SK Nürnberg']
    df7TIWnbg.loc[:,'Date'] = pd.to_datetime(df7TIWnbg['Date'], format='%Y%m%d')

    #Wetterdaten für Nbg holen
    API = Wetterdienst("dwd", "observation")

    request = API(
        parameter=["climate_summary"],
        resolution="daily",
        start_date="2020-04-02",  # Timezone: UTC
        end_date=today,  # Timezone: UTC
        tidy_data=True,  # default
        humanize_parameters=True,  # default
    ).filter(station_id=[3668]) #Wetter für Nbg
    stations = request.df
    values = request.values.all().df
    values = values.loc[values['PARAMETER'] == 'SUNSHINE_DURATION']

    #Corona Restriktionen holen / später für Bayern?
    dfCoronaRestr = pd.read_csv('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv')
    dfCoronaRestr = dfCoronaRestr[dfCoronaRestr.CountryName == 'Germany']
    stringency = dfCoronaRestr[['Date','StringencyIndexForDisplay']]

    return df7TIWnbg,values,stringency

def FeiertageHolen():
    # Feiertage holen
    holidaysdf2020datum = pd.read_json('https://feiertage-api.de/api/?jahr=2020&nur_daten',orient='index')
    holidaysdf2021datum = pd.read_json('https://feiertage-api.de/api/?jahr=2021&nur_daten',orient='index') 
    holidaysdf2020datum.columns = ['RefDay']
    holidaysdf2021datum.columns = ['RefDay']
    holydaysComp = pd.concat([holidaysdf2020datum,holidaysdf2021datum]).fillna(0)
    holydaysComp.to_csv('holydays.csv')

CoronaDatenNbg, Wetterdaten, Restriktionen = DatenVergangenheitHolen()