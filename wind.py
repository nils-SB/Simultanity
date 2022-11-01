"""
This programm is supposed to calculate the Wind-Generation for a given Dataset of windspeeds
"""

import pandas as pd
from datetime import date, timedelta, datetime
from StationData import get_station


class siemens(object):
    def output(self, wind_speed, hub_height, station_height=8, height_exp=0.10):
        koeff = (hub_height / station_height) ** height_exp  # Hellmannscher Höhenexponent 0.16 für Küste
        # koeff = 1/math.log(station_height/0.2)*math.log(hub_height/0.2)
        wind_speed['wind_speed_hubheight'] = wind_speed['wind_speed'] * koeff
        POWER_CURVE = {
            0: 0,
            1: 0,
            2: 0,
            3: 90,
            3.5: 181,
            4: 333,
            4.5: 530,
            5: 769,
            5.5: 1054,
            6: 1394,
            6.5: 1794,
            7: 2259,
            7.5: 2792,
            8: 3387,
            8.5: 4020,
            9: 4651,
            9.5: 5228,
            10: 5705,
            10.5: 6060,
            11: 6297,
            11.5: 6440,
            12: 6520,
            12.5: 6561,
            13: 6582,
            13.5: 6592,
            14: 6596,
            14.5: 6598,
            15: 6599,
            15.5: 6600,
            16: 6600,
            16.5: 6600,
            17: 6600,
            17.5: 6600,
            18: 6600,
            18.5: 6600,
            19: 6600,
            19.5: 6600,
            20: 6600,
            20.5: 6468,
            21: 6336,
            21.5: 6204,
            22: 6072,
            22.5: 5940,
            23: 5808,
            23.5: 5676,
            24: 5544,
            24.5: 5412,
            25: 5280,
        }
        wind_speed.loc[(wind_speed['wind_speed_hubheight'] <= 3), 'WEA_Power'] = POWER_CURVE.get(0)
        for j in range(2 * 3, 2 * 25):
            i = j / 2
            p_i = POWER_CURVE.get(i)
            p_i1 = POWER_CURVE.get((i + 0.5))
            delta = p_i1 - p_i
            wind_speed.loc[(wind_speed['wind_speed_hubheight'] >= i) & (
                    wind_speed['wind_speed_hubheight'] <= (i + 1)), 'WEA_Power'] = POWER_CURVE.get(i) + (wind_speed[
                                                                                                             'wind_speed_hubheight'] - i) * delta
        wind_speed.loc[(wind_speed['wind_speed_hubheight'] >= 25), 'WEA_Power'] = POWER_CURVE.get(0)
        return wind_speed


class nordex(object):
    def output(self, wind_speed, hub_height, station_height=8, height_exp=0.10):
        koeff = (hub_height / station_height) ** height_exp  # Hellmannscher Höhenexponent 0.16 für Küste
        # koeff = 1/math.log(station_height/0.2)*math.log(hub_height/0.2)
        wind_speed['wind_speed_hubheight'] = wind_speed['wind_speed'] * koeff
        POWER_CURVE = {
            0: 0,
            1: 0,
            2: 0,
            3: 31,
            3.5: 116,
            4: 239,
            4.5: 392,
            5: 574,
            5.5: 790,
            6: 1045,
            6.5: 1345,
            7: 1693,
            7.5: 2093,
            8: 2549,
            8.5: 3061,
            9: 3604,
            9.5: 4150,
            10: 4662,
            10.5: 5056,
            11: 5341,
            11.5: 5530,
            12: 5645,
            12.5: 5697,
            13: 5700,
            13.5: 5700,
            14: 5700,
            14.5: 5700,
            15: 5700,
            15.5: 5700,
            16: 5700,
            16.5: 5700,
            17: 5700,
            17.5: 5700,
            18: 5700,
            18.5: 5700,
            19: 5700,
            19.5: 5700,
            20: 5700,
            20.5: 5700,
            21: 5700,
            21.5: 5700,
            22: 5700,
            22.5: 5603,
            23: 5506,
            23.5: 5387,
            24: 5278,
            24.5: 5147,
            25: 5039,
            25.5: 4891,
            26: 4748,
        }
        wind_speed.loc[(wind_speed['wind_speed_hubheight'] <= 3), 'WEA_Power'] = POWER_CURVE.get(0)
        for j in range(2 * 3, 2 * 26):
            i = j / 2
            p_i = POWER_CURVE.get(i)
            p_i1 = POWER_CURVE.get((i + 0.5))
            delta = p_i1 - p_i
            wind_speed.loc[(wind_speed['wind_speed_hubheight'] >= i) & (
                    wind_speed['wind_speed_hubheight'] <= (i + 1)), 'WEA_Power'] = POWER_CURVE.get(i) + (wind_speed[
                                                                                                             'wind_speed_hubheight'] - i) * delta
        wind_speed.loc[(wind_speed['wind_speed_hubheight'] >= 26), 'WEA_Power'] = POWER_CURVE.get(0)
        return wind_speed


_WEA_TYPES = {
    'SG 6.6-170': siemens,
    'Nordex N149/5.7': nordex,
}


def run_model(data, hub_height, windturbine, height_exp=0.10):
    WEA_class = _WEA_TYPES[windturbine]
    WEA = WEA_class()
    out = WEA.output(wind_speed=data, hub_height=hub_height, height_exp=height_exp)
    return out

def quater_hour(data_frame):
    re_df = pd.DataFrame()
    if 'wind_speed' in data_frame.columns:
        winds = data_frame['wind_speed'].resample("15Min", closed="left").mean()
        re_df['wind_speed'] = winds
    return re_df


def windMinutes(start_str, end_str, station, include_raw_data, quarterly, historic):
    """

    :param historic:
    :param quarterly: Boolean value. Decides if the weather Data is processed in 15 Minutes or 10 Minutes
    :param start_str: integer Value which is the Datetime Format from the DWD in Format YYYYMMDDHHMM
    :param end_str: integer Value which is the Datetime Format from the DWD in Format YYYYMMDDHHMM
    :param station: which of the Stations in StationData.py is chosen
    :param include_raw_data: Boolean value. Decides if you want to include irradiance data in output Dataframe
    :return: Dataframe with simulation results. Index = datetime index, PV_output = PV_output in W,
             if include_raw_data=True direct= direct irradiance in Wh/m^2, diffuse= diffuse irradiance in Wh/m^2,
             temp= Temperatur in °C
    """
    station_dict = get_station(station=station, historic=historic)
    read_data = pd.read_csv(filepath_or_buffer=
                            station_dict['wind_url'],
                            sep=';', na_values='-999')
    data = read_data[['FF_10', 'MESS_DATUM']].copy()
    data.rename(columns={'FF_10': 'wind_speed'}, inplace=True)
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
    df = run_model(data, hub_height=station_dict['hub_height'], windturbine=station_dict['windturbine']
                   , height_exp=station_dict['height_exp'])
    if not include_raw_data:
        df.drop(columns=['wind_speed', 'wind_speed_hubheight'], inplace=True)
    return df


if __name__ == '__main__':
    start = 201001010000
    end = 201101010000
    df_w = windMinutes(start_str=start, end_str=end, station="st. peter ording", include_raw_data=True)
    df_w.to_excel('Wind.xlsx', sheet_name='sheet0', index=True)
