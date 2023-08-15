# -*- coding: utf-8 -*-
"""Weather_Data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1py-Slt4IX6JwVLh2d8JmutUsOARJBaER
"""

"""
Team members: Deepika Gonela, Pandre Vamshi, Krishna Tej Alahari, Akshith Reddy Kota
General description of the code: This code queries the NOAA GSOD dataset and creates a weather csv file that contains data from all the weather stations across the European Union.
System used to run the code: Google Colab

"""

import bq_helper
from bq_helper import BigQueryHelper
import pandas as pd

# create BigQueryHelper objects for the NOAA GSOD dataset in the bigquery-public-data and fh-bigquery projects
noaa = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="ghcn_d")

noaa = bq_helper.BigQueryHelper(active_project="fh-bigquery",
                                   dataset_name="weather_gsod")

# create a BigQueryHelper object for the NOAA GSOD dataset in the bigquery-public-data project
bq_assistant = BigQueryHelper("bigquery-public-data", "noaa_gsod")

df=pd.DataFrame(bq_assistant.head("stations"))

# create a list of the European Union country codes
european_union = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK']

# create an empty DataFrame to hold the weather data
data = pd.DataFrame()

# loop through each European Union country and query weather data for 2015-2018
for each in european_union:
    QUERY15 = """select state, name, min(stn), min(year), mo, avg(temp), avg(lat), avg(lon), avg(max), avg(prcp), avg(sndp) from`bigquery-public-data.noaa_gsod.stations` b JOIN `bigquery-public-data.noaa_gsod.gsod2015`a 
    ON a.wban=b.wban AND a.stn=b.usaf where b.country = '{}' group by state, name, mo""".format(each)
    weather15 = bq_assistant.query_to_pandas(QUERY15)

    QUERY16 = """select state, name, min(stn), min(year), mo, avg(temp), avg(lat), avg(lon), avg(max), avg(prcp), avg(sndp) from`bigquery-public-data.noaa_gsod.stations` b JOIN `bigquery-public-data.noaa_gsod.gsod2016`a 
    ON a.wban=b.wban AND a.stn=b.usaf where b.country = '{}' group by state, name, mo""".format(each)
    weather16= bq_assistant.query_to_pandas(QUERY16)


    QUERY17 =  """select state, name, min(stn), min(year), mo, avg(temp), avg(lat), avg(lon), avg(max), avg(prcp), avg(sndp) from`bigquery-public-data.noaa_gsod.stations` b JOIN `bigquery-public-data.noaa_gsod.gsod2017`a 
    ON a.wban=b.wban AND a.stn=b.usaf where b.country = '{}' group by state, name, mo""".format(each)
    weather17= bq_assistant.query_to_pandas(QUERY17)

    QUERY18 = """select state, name, min(stn), min(year), mo, avg(temp), avg(lat), avg(lon), avg(max), avg(prcp), avg(sndp) from`bigquery-public-data.noaa_gsod.stations` b JOIN `bigquery-public-data.noaa_gsod.gsod2018`a 
    ON a.wban=b.wban AND a.stn=b.usaf where b.country = '{}' group by state, name, mo""".format(each)
    
    weather18= bq_assistant.query_to_pandas(QUERY18)
    temp = pd.concat([weather15, weather16, weather17, weather18])
    temp['country'] = each
    data = pd.concat([data, temp])

    
data.columns = ['state','name', 'station', 'year', 'month', 'avg_temp','avg_lat', 'avg_lon', 'avg_max_temp', 'avg_prcp', 'avg_snow_depth', 'country']

data.to_csv('weather.csv', index = False)