import pandas as pd 
import glob

download_dates = pd.date_range(start='20200402', end='20210307').strftime('%Y%m%d')

base_url = ("https://www.lgl.bayern.de/gesundheit/infektionsschutz/infektionskrankheiten_a_z/coronavirus/karte_coronavirus/fallzahlen_archiv/")

list_of_url = [base_url+date+str('_LK_coronazahlen.csv') for date in download_dates]

df = pd.DataFrame()

for url, date in zip(list_of_url,download_dates):
    try:
        tempdf = pd.read_csv(url, encoding='latin-1',delimiter=';')
        tempdf['Date'] = date
        df = pd.concat([df, tempdf])
    except:
        print(str('no data for')+url)

df.to_csv('LK_coronazahlen20200402_20210307.csv')