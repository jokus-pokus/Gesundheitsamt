import pandas as pd 
import glob
from datetime import date
from wetterdienst import Wetterdienst
import geopandas as gpd
from wetterdienst import Wetterdienst, Resolution, Period
import streamlit as st 
from wetterdienst.dwd.forecasts import DwdMosmixType


import requests
import json
import numpy as np

today = date.today()
print("Today's date:", today)

#@st.cache
def DatenVergangenheitHolen():

    # Daten des 7TIW holen
    #dfgeo = gpd.read_file('https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.geojson',ignore_geometry=True)
    #dfgeo = gpd.read_file("https://opendata.arcgis.com/datasets/45258e51f57d43efb612f700a876ae8f_0.geojson",ignore_geometry=True)
    dfgeo = pd.read_csv("https://opendata.arcgis.com/api/v3/datasets/45258e51f57d43efb612f700a876ae8f_0/downloads/data?format=csv&spatialRefId=4326")
    dfgeo = dfgeo.loc[dfgeo['Landkreis'] == 'SK Nürnberg']
    dfgeo = dfgeo.groupby(['Refdatum']).sum()
    dfgeo = dfgeo.reset_index()
    df1 = pd.DataFrame(dfgeo)
    df1['Summe7Tage'] = df1.AnzahlFall.rolling(min_periods=1, window=7).sum()
    df1['7TIW'] = (df1.Summe7Tage/518000)*100000
    df1 = df1[['Refdatum','7TIW']]

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
    values = values.loc[values['PARAMETER'] == 'TEMPERATURE_AIR_200']

    #Corona Restriktionen holen / später für Bayern?
    dfCoronaRestr = pd.read_csv('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv')
    dfCoronaRestr = dfCoronaRestr[dfCoronaRestr.CountryName == 'Germany']
    stringency = dfCoronaRestr[['Date','StringencyIndexForDisplay']]

    return df1,values,stringency

def FeiertageHolen():
    # Feiertage holen
    holidaysdf2020datum = pd.read_json('https://feiertage-api.de/api/?jahr=2020&nur_daten',orient='index')
    holidaysdf2021datum = pd.read_json('https://feiertage-api.de/api/?jahr=2021&nur_daten',orient='index') 
    holidaysdf2020datum.columns = ['Date']
    holidaysdf2021datum.columns = ['Date']
    holydaysComp = pd.concat([holidaysdf2020datum,holidaysdf2021datum]).fillna(0)
    #holydaysComp.to_csv('holydays.csv')
    return holydaysComp


def WetterVorhersageNBG():
    API = Wetterdienst(provider="dwd", kind="forecast")
    stations = API(mosmix_type=DwdMosmixType.SMALL).filter(station_id="10763") #Station ID ist anders als bei den Historischendaten... völlig klar
    df = stations.values.all().df
    df = df[df['PARAMETER']=='TEMPERATURE_AIR_200']
    df['VALUE'] = df['VALUE'] - 273.15
    df['date'] = df['DATE'].dt.date
    df = df.groupby('date').mean()
    return df

#CoronaDatenNbg, Wetterdaten, Restriktionen = DatenVergangenheitHolen()
#CoronaDatenNbg.head()
