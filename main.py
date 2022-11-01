# Auomated runs to simulate the Simultanity of Generation
import pandas as pd
import json
from pv_sim import pvMinutes
from wind import windMinutes
from sqlalchemy import create_engine
from datetime import datetime
from StationData import get_station

# Credentials to database connection
hostname = "localhost"
dbname = "SimultanityDB"
uname = "root"
pwd = "root"


def read_json_obj(path: str):
    """
    Extract an object from a json file.
    :return: obj: parsed json object
    """
    # read file
    with open(path, 'r') as jsonFile:
        json_data = jsonFile.read()
    # parse file
    obj = json.loads(json_data)
    return obj


def kpi_matrix(data, station):
    setup_dict = read_json_obj("JSON_Config.JSON")
    years = (201001010000, 201101010000, 201201010000, 201301010000, 201401010000, 201501010000, 201601010000,
             201701010000, 201801010000, 201901010000, 201912312350)
    kpi_dict = {2010: {}, 2011: {}, 2012: {}, 2013: {}, 2014: {}, 2015: {}, 2016: {}, 2017: {}, 2018: {}, 2019: {}}
    station_dict = get_station(station=station, historic=False)
    for i in range(0, 10):
        dtstart = datetime.strptime(str(years[i]), '%Y%m%d%H%M')
        dtend = datetime.strptime(str(years[i + 1]), '%Y%m%d%H%M')
        yeardf = data[dtstart:dtend]
        kpi_dict[dtstart.year]['Volllaststunden PV'] = yeardf['PV_output'].sum() / 6 / (
                station_dict['pv_cap'] / 0.83333)
        kpi_dict[dtstart.year]['Volllaststunden Wind'] = yeardf['WEA_Power'].sum() / 6 / station_dict[
            'pv_cap']  # PV_cap = WEA Nennleistung. Ist hier gleichwertig
        if setup_dict['simulation']["include_raw_data"]:
            kpi_dict[dtstart.year]['Mittlere Windgeschwindigkeit auf Nabenhöhe'] = yeardf['wind_speed_hubheight'].mean()
            kpi_dict[dtstart.year]['Summe der Solarenstrahlung'] = (yeardf['direct'].sum() + yeardf[
                'diffuse'].sum()) / 6 / 1000
        kpi_dict[dtstart.year]['g > 0.5 in %'] = sum((yeardf['power_total'] / station_dict['pv_cap']) > 1) / \
                                                 yeardf.shape[
                                                     0] * 100
        over = yeardf['power_total'] > station_dict['pv_cap']
        e_cap = yeardf['power_total'].copy()
        e_cap[over] = station_dict['pv_cap']
        e_over = sum(yeardf['power_total'][over])
        e_total = yeardf['power_total'].sum()
        kpi_dict[dtstart.year]['Verlust bei g > 0.5 in %'] = (e_total - e_cap.sum()) / e_total * 100
        kpi_dict[dtstart.year]['Verlust bei g > 0.5 normiert auf Nennleistung'] = \
            (e_total - e_cap.sum()) / 6 / station_dict['pv_cap']
        kpi_dict[dtstart.year]['Missing Datapoints'] = yeardf['power_total'].isnull().sum()
        kpi_dict[dtstart.year]['Missing Datapoints in %'] = yeardf['power_total'].isnull().sum() / yeardf.shape[0] * 100
        # db = '{Standort}_historical'.format(Standort=setup_dict['simulation']['station'])
    kpi_df = pd.DataFrame.from_dict(kpi_dict, orient='index')
    return kpi_df


def get_da_data(year):
    if year == 2019:
        read_data = pd.read_csv(filepath_or_buffer=
                                "C:/Users/nilsb/Data/Marktdaten/StromMarkt/DA_2019.csv",
                                sep=';', na_values='-999')
    elif year == 2020:
        read_data = pd.read_csv(filepath_or_buffer=
                                "C:/Users/nilsb/Data/Marktdaten/StromMarkt/DA_2020.csv",
                                sep=';', na_values='-999')
    elif year == 2021:
        read_data = pd.read_csv(filepath_or_buffer=
                                "C:/Users/nilsb/Data/Marktdaten/StromMarkt/DA_2021.csv",
                                sep=';', na_values='-999')
    else:
        raise ValueError('Jahr nicht vorhanden')
    format = '%d.%m.%Y %H:%M'
    read_data['Datetime'] = pd.to_datetime(read_data['Datum'] + ' ' + read_data['Uhrzeit'], format=format)
    read_data = read_data.set_index(pd.DatetimeIndex(read_data['Datetime']))
    read_data.drop(columns=['Datum', 'Uhrzeit', 'Datetime'], inplace=True)
    read_data = read_data.resample("15Min").mean().ffill()
    read_data.rename(columns={'Deutschland/Luxemburg[€/MWh]': 'DA[€/MWh]'}, inplace=True)
    return read_data


if __name__ == '__main__':
    setup_dict = read_json_obj("JSON_Config.JSON")  # ACHTUNG !!! HIER DARAUF ACHTEN
    station = setup_dict["simulation"]["station"]
    # Create SQLAlchemy engine to connect to MySQL Database
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                           .format(host=setup_dict["database"]["hostname"],
                                   db=setup_dict["database"]["dbname"],
                                   user=setup_dict["database"]["uname"],
                                   pw=setup_dict["database"]["pwd"]), pool_pre_ping=True)
    start = setup_dict["simulation"]["start"]
    end = setup_dict["simulation"]["end"]
    if setup_dict["simulation"]["15min"] and setup_dict["simulation"]["historic"]:
        start = 201901010000
        end = 201912312350
    print(f"{datetime.now()} - Starting PV simulation ")
    df_PV = pvMinutes(start_str=start, end_str=end, station=station
                      , include_raw_data=setup_dict['simulation']["include_raw_data"],
                      south=setup_dict['simulation']["south"], quarterly=setup_dict["simulation"]["15min"],
                      historic=setup_dict['simulation']["historic"])
    print(f"{datetime.now()} - Finished PV simulation ")
    if 'temperature' in df_PV.columns:
        df_PV.drop(columns='temperature', inplace=True)
    df_PV['PV_output'] = df_PV['PV_output'] / 1000
    print(f"{datetime.now()} - Starting Wind simulation ")
    df_Wind = windMinutes(start_str=start, end_str=end, station=station,
                          include_raw_data=setup_dict['simulation']["include_raw_data"],
                          quarterly=setup_dict["simulation"]["15min"], historic=setup_dict['simulation']["historic"])
    print(f"{datetime.now()} - Finished Wind simulation ")
    df = pd.concat([df_PV, df_Wind], axis=1)
    df['power_total'] = df['PV_output'] + df['WEA_Power']
    if setup_dict["simulation"]["15min"]:
        year = datetime.strptime(str(start), '%Y%m%d%H%M').year
        da_df = get_da_data(year)
        df['revenue'] = df['power_total']/1000 * da_df['DA[€/MWh]']/4
    print(f"{datetime.now()} - Writing to SQL ")
    # Convert dataframe to sql table
    df.to_sql('{Standort}_{name}'.format(Standort=station, name=setup_dict["simulation"]["save"])
              , engine, index=True, if_exists='replace')
    # hier df in SQL wegschreiben jdbc:mysql://localhost:3306/SimultanityDB
    print(f"{datetime.now()} - Finished writing to SQL ")
    if not setup_dict["simulation"]["15min"]:
        print(f"{datetime.now()} - KPI-Matrix ")
        kpi_df = kpi_matrix(data=df, station=station)
        print(f"{datetime.now()} - Writing KPI-Matrix to SQL")
        kpi_df.to_sql('{Standort}_{name}_kpi'.format(Standort=station, name=setup_dict["simulation"]["save"])
                      , engine, index=True, if_exists='replace')
        print(f"{datetime.now()} - Finished Writing KPI-Matrix to SQL")
