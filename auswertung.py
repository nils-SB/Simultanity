import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from main import read_json_obj
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, timedelta, datetime
from StationData import get_station


def draw_heatmap(data):
    fig = plt.figure()
    newdf = data[['power_total', 'PV_output', 'WEA_Power']].copy()
    newdf['date'] = data.index.date
    newdf['time'] = data.index.time
    newdf = newdf.pivot('time', 'date', 'power_total')
    ax = sns.heatmap(newdf, cmap='turbo', linewidths=.005, linecolor='black')
    plt.show()


def get_hull(data):
    years = (201001010000, 201101010000, 201201010000, 201301010000, 201401010000, 201501010000, 201601010000,
             201701010000, 201801010000, 201901010000, 201912312350)
    pv_array = np.zeros([10, 365])
    wind_array = np.zeros([10, 365])
    total_array = np.zeros([10, 365])
    over_array = np.zeros([10, 365])
    for i in range(0, 10):
        dtstart = datetime.strptime(str(years[i]), '%Y%m%d%H%M')
        dtend = datetime.strptime(str(years[i + 1]), '%Y%m%d%H%M')
        yeardf = data[dtstart:dtend]
        newdf = yeardf[['power_total', 'PV_output', 'WEA_Power']].copy()
        newdf['day'] = newdf.index.dayofyear
        for day in range(1, 366):
            temp = newdf.loc[newdf['day'] == day]
            pv_array[i][day - 1] = temp['PV_output'].sum()
            wind_array[i][day - 1] = temp['WEA_Power'].sum()
            total_array[i][day - 1] = temp['power_total'].sum()
            over_array[i][day - 1] = (temp['power_total'] / newdf['power_total'].max() > 0.5).sum()/(24*6) * 100
    pv_mean = np.zeros([365, 3])
    wind_mean = np.zeros([365, 3])
    total_mean = np.zeros([365, 3])
    over_sum = np.zeros([365, 3])
    pv_array = pv_array / pv_array.max()
    wind_array = wind_array / wind_array.max()
    total_array = total_array / total_array.max()
    for day in range(1, 366):
        pv_mean[day - 1, 0] = pv_array[:, day - 1].mean()
        pv_mean[day - 1, 1] = pv_array[:, day - 1].min()
        pv_mean[day - 1, 2] = pv_array[:, day - 1].max()

        wind_mean[day - 1, 0] = wind_array[:, day - 1].mean()
        wind_mean[day - 1, 1] = wind_array[:, day - 1].min()
        wind_mean[day - 1, 2] = wind_array[:, day - 1].max()

        total_mean[day - 1, 0] = total_array[:, day - 1].mean()
        total_mean[day - 1, 1] = total_array[:, day - 1].min()
        total_mean[day - 1, 2] = total_array[:, day - 1].max()

        over_sum[day - 1, 0] = over_array[:, day - 1].mean()
        over_sum[day - 1, 1] = over_array[:, day - 1].min()
        over_sum[day - 1, 2] = over_array[:, day - 1].max()
    hull_dict = {'pv': pv_mean, 'wind': wind_mean, 'total': total_mean, 'over': over_sum}
    return hull_dict


def kpi_matrix():
    years = (201001010000, 201101010000, 201201010000, 201301010000, 201401010000, 201501010000, 201601010000,
             201701010000, 201801010000, 201901010000, 201912312350)
    kpi_dict = {2010: {}, 2011: {}, 2012: {}, 2013: {}, 2014: {}, 2015: {}, 2016: {}, 2017: {}, 2018: {}, 2019: {}}
    station_dict = get_station(station=setup_dict['simulation']['station'])
    for i in range(0, 10):
        dtstart = datetime.strptime(str(years[i]), '%Y%m%d%H%M')
        dtend = datetime.strptime(str(years[i + 1]), '%Y%m%d%H%M')
        yeardf = df[dtstart:dtend]
        kpi_dict[dtstart.year]['Volllaststunden PV'] = yeardf['PV_output'].sum() / 6 / (
                station_dict['pv_cap'] / 0.83333)
        kpi_dict[dtstart.year]['Volllaststunden Wind'] = yeardf['WEA_Power'].sum() / 6 / station_dict[
            'pv_cap']  # PV_cap = WEA Nennleistung. Ist hier gleichwertig
        if setup_dict['simulation']["include_raw_data"]:
            kpi_dict[dtstart.year]['Mittlere Windgeschwindigkeit auf Nabenhöhe'] = yeardf['wind_speed_hubheight'].mean()
            kpi_dict[dtstart.year]['Summe der Solarenstrahlung'] = (yeardf['direct'].sum() + yeardf[
                'diffuse'].sum()) / 6 / 1000
        kpi_dict[dtstart.year]['g > 1 in %'] = sum((yeardf['power_total'] / station_dict['pv_cap']) > 1) / yeardf.shape[
            0] * 100
        over = yeardf['power_total'] > station_dict['pv_cap']
        e_cap = yeardf['power_total'][not over]
        e_cap[over] = station_dict['pv_cap']
        e_over = sum(yeardf['power_total'][over])
        e_total = yeardf['power_total'].sum()
        kpi_dict[dtstart.year]['Verlust bei g > 1 in %'] = e_over / e_total * 100
        kpi_dict[dtstart.year]['Verlust bei g > 1 in kW'] = e_over
        kpi_dict[dtstart.year]['Missing Datapoints'] = yeardf['power_total'].isnull().sum()
        kpi_dict[dtstart.year]['Missing Datapoints in %'] = yeardf['power_total'].isnull().sum() / yeardf.shape[0]
        # db = '{Standort}_historical'.format(Standort=setup_dict['simulation']['station'])
    kpi_db = pd.DataFrame(kpi_dict)
    return kpi_db


if __name__ == '__main__':
    setup_dict = read_json_obj("JSON_Config.JSON")
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                           .format(host=setup_dict["database"]["hostname"],
                                   db=setup_dict["database"]["dbname"],
                                   user=setup_dict["database"]["uname"],
                                   pw=setup_dict["database"]["pwd"]))
    db = '{Standort}_historical'.format(Standort=setup_dict['simulation']['station'])
    df = pd.read_sql(db, engine)
    df.set_index(['datetime_index'], inplace=True)
    yeardf = df['2010-01-01':'2010-12-31']
    draw_heatmap(yeardf)
    dtstart = datetime.strptime(str(201001010000), '%Y%m%d%H%M')
