# This programm is supposed to calculate the PV-Generation for a given Dataset of Radiation

import pandas as pd
from datetime import date, timedelta, datetime
import wind
from pv import run_model
from StationData import get_station


def quater_hour(data_frame):
    re_df = pd.DataFrame()
    if 'global_horizontal' in data_frame.columns:
        solar = data_frame[['diffuse_fraction', 'global_horizontal']].copy()
        solar_5min = solar.resample("5Min").ffill() / 2
        solar = solar_5min.resample("15Min", closed="left").sum()
        re_df = solar * 4/6
    if 'temperature' in data_frame.columns:
        temper = data_frame['temperature'].resample("15Min", closed="left").mean()
        re_df['temperature'] = temper
    return re_df


def pvMinutes(start_str, end_str, station, include_raw_data, south, quarterly, historic):
    """
    Simulates PV yield based on DWD weather data, based on pv.py code. Funktion reads weather data and
    fixes indexing.
    :param historic:
    :param quarterly: Boolean value. Decides if the weather Data is processed in 15 Minutes or 10 Minutes
    :param south: Boolean value. Decides if the PV is facing south
    :param include_raw_data: Boolean value. Decides if you want to include irradiance data in output Dataframe
    :param start_str: integer Value which is the Datetime Format from the DWD in Format YYYYMMDDHHMM
    :param end_str: integer Value which is the Datetime Format from the DWD in Format YYYYMMDDHHMM
    :param station: which of the Stations in StationData.py is chosen
    :return: Dataframe with simulation results. Index = datetime index, PV_output = PV_output in W,
             if include_raw_data=True direct= direct irradiance in Wh/m^2, diffuse= diffuse irradiance in Wh/m^2,
             temp= Temperatur in °C
    """
    station_dict = get_station(station=station, historic=historic)
    read_data = pd.read_csv(filepath_or_buffer=
                            station_dict['solar_url'],
                            sep=';', na_values='-999')
    data = 16.667 * read_data[['DS_10', 'GS_10']]  # J/cm^2= 2,7778 Wh/m^2 Daten liegen als summe über 10min vor
    data['MESS_DATUM'] = read_data['MESS_DATUM']
    data['global_horizontal'] = data['GS_10'] - data['DS_10']
    data.rename(columns={'DS_10': 'diffuse_fraction'}, inplace=True)
    read_data = pd.read_csv(filepath_or_buffer=
                            station_dict['temp_url'],
                            sep=';', na_values='-999')
    data['temperature'] = read_data['TT_10']
    start = data.loc[data['MESS_DATUM'] == start_str].index[0]
    end = data.loc[data['MESS_DATUM'] == end_str].index[0]
    data = data[start:end]
    index = []
    delta = (end - start)
    dtstart = datetime.strptime(str(start_str), '%Y%m%d%H%M')
    for i in range(0, delta):
        index.append(dtstart + timedelta(minutes=i * 10))
    data.insert(0, 'datetime_index', index)
    data.set_index(['datetime_index'], inplace=True)
    data.index = pd.to_datetime(data.index)
    data.drop(columns='MESS_DATUM', inplace=True)
    if quarterly:
        data = quater_hour(data)
    cap = station_dict['pv_cap'] / 0.83333  # PV Capacity in kWp
    if south:
        dfpv = run_model(data=data, coords=station_dict['coords'],
                         tilt=20, azim=180, tracking=0,
                         capacity=cap * 1000, include_raw_data=include_raw_data,
                         inverter_capacity=station_dict['pv_cap'] / 0.95 * 1000, system_loss=0.05)
    else:
        cap = cap / 2  # half of the capacity is facing east, half west
        df_east = run_model(data=data, coords=station_dict['coords'],
                            tilt=10, azim=90, tracking=0,
                            capacity=cap * 1000, include_raw_data=include_raw_data,
                            inverter_capacity=station_dict['pv_cap'] / 2 / 0.95 * 1000, system_loss=0.05)
        df_west = run_model(data=data, coords=station_dict['coords'],
                            tilt=10, azim=270, tracking=0,
                            capacity=cap * 1000, include_raw_data=include_raw_data,
                            inverter_capacity=station_dict['pv_cap'] / 2 / 0.95 * 1000, system_loss=0.05)
        dfpv = df_east
        dfpv["PV_output"] = df_east["PV_output"] + df_west["PV_output"]
    return dfpv


if __name__ == '__main__':
    stations = 'st. peter ording'
    start = 201001010000
    end = 201101010000
    df_PV = pvMinutes(start_str=start, end_str=end, station=stations, south=True, include_raw_data=True)
    df_PV.drop(columns='temperature', inplace=True)
    df_PV['PV_output'] = df_PV['PV_output'] / 1000
    df_Wind = wind.windMinutes(start_str=start, end_str=end, station=stations, include_raw_data=True)
    df = pd.concat([df_PV, df_Wind], axis=1)
    df['power_total'] = df['PV_output'] + df['WEA_Power']
    df.to_excel('C:/Users/nilsb/Data/Wetterdaten/St. Peter Ording/2010_south.xlsx', sheet_name='sheet0', index=True)
