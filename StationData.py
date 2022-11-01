# Station data

def get_station(station, historic=True):
    """
    Function returns data based on what Weather Station is simulated.
    :param historic:
    :param station:
    :return: answer_dict{ -> Dictionary containing:
                solar_url: Where is the Solar irradiance data stored
                temp_url: Where is the Temperature data stored
                wind_url: Where is the wind data stored
                coords: What are the coordinates of the Station
                height_exp: Value to extrapolate the windspeed to hub height
                windturbine: Which windturbine model is chosen for the location
                hub_height: How high is the hub
                pv_cap: How high is the installed PV capacity. Is chosen to match the WEA capacity
                }
    """
    answer_dict = {}
    if station == 'st. peter ording':
        answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/St. Peter Ording/Solar/2010-2019/10MinPVStPeter.txt"
        answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/St. Peter Ording/Temperatur/10MinTempStPeter.txt"
        answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/St. Peter Ording/Wind/2010-2019/10MinWindStPeter.txt"
        answer_dict['coords'] = (54.3279, 8.6031)
        answer_dict['height_exp'] = 0.10
        answer_dict['windturbine'] = "SG 6.6-170"
        answer_dict['hub_height'] = 115
        answer_dict['pv_cap'] = 6600
    elif station == 'marnitz':
        answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/Marnitz/Solar/2010-2019/10MinPVMarnitz.txt"
        answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/Marnitz/Temperatur/10MinTempMarnitz.txt"
        answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/Marnitz/Wind/2010-2019/10MinWindMarnitz.txt"
        answer_dict['coords'] = (53.3222, 11.9321)
        answer_dict['height_exp'] = 0.23
        answer_dict['windturbine'] = 'Nordex N149/5.7'
        answer_dict['hub_height'] = 150
        answer_dict['pv_cap'] = 5700
    elif station == 'leck':
        answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/Leck/Solar/2010-2019/10MinPVLeck.txt"
        answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/Leck/Temperatur/10MinTempLeck.txt"
        answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/Leck/Wind/2010-2019/10MinWindLeck.txt"
        answer_dict['coords'] = (54.7903, 8.9514)
        answer_dict['height_exp'] = 0.16
        answer_dict['windturbine'] = "SG 6.6-170"
        answer_dict['hub_height'] = 150
        answer_dict['pv_cap'] = 6600
    elif station == 'greifswald':
        answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/Greifswald/Solar/10MinSolarGreifswald.txt"
        answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/Greifswald/Temperatur/10MinTempGreifswald.txt"
        answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/Greifswald/Wind/10MinWindGreifswald.txt"
        answer_dict['coords'] = (54.0967, 13.4056)
        answer_dict['height_exp'] = 0.23
        answer_dict['windturbine'] = 'Nordex N149/5.7'
        answer_dict['hub_height'] = 150
        answer_dict['pv_cap'] = 5700
    elif station == 'schwerin':
        answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/Schwerin/Solar/10MinSolarSchwerin.txt"
        answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/Schwerin/Temperatur/10MinTempSchwerin.txt"
        answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/Schwerin/Wind/10MinWindSchwerin.txt"
        answer_dict['coords'] = (53.6424, 11.3871)
        answer_dict['height_exp'] = 0.23
        answer_dict['windturbine'] = 'Nordex N149/5.7'
        answer_dict['hub_height'] = 150
        answer_dict['pv_cap'] = 5700
    elif station == 'angermuende':
        if historic:
            answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/Angermünde/Solar/10MinSolarAnger.txt"
            answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/Angermünde/Temperatur/10MinTempAnger.txt"
            answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/Angermünde/Wind/10MinWindAnger.txt"
        else:
            answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/Angermünde/Solar/10MinSolar2020+.txt"
            answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/Angermünde/Temperatur/10MinTemp2020+.txt"
            answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/Angermünde/Wind/10MinWind2020+.txt"
        answer_dict['coords'] = (53.0316, 13.9908)
        answer_dict['height_exp'] = 0.23
        answer_dict['windturbine'] = 'Nordex N149/5.7'
        answer_dict['hub_height'] = 150
        answer_dict['pv_cap'] = 5700
    elif station == 'doernick':
        answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/Dörnick/Solar/10MinSolarDornick.txt"
        answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/Dörnick/Temperatur/10MinTempDoernick.txt"
        answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/Dörnick/Wind/10MinWindDornick.txt"
        answer_dict['coords'] = (54.1654, 10.3519)
        answer_dict['height_exp'] = 0.23
        answer_dict['windturbine'] = 'Nordex N149/5.7'
        answer_dict['hub_height'] = 150
        answer_dict['pv_cap'] = 5700
    elif station == 'bremervoerde':
        answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/Bremervörde/Solar/10MinSolarBre.txt"
        answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/Bremervörde/Temperatur/10MinTempBre.txt"
        answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/Bremervörde/Wind/10MinWindBre.txt"
        answer_dict['coords'] = (53.4451, 9.1390)
        answer_dict['height_exp'] = 0.23
        answer_dict['windturbine'] = 'Nordex N149/5.7'
        answer_dict['hub_height'] = 150
        answer_dict['pv_cap'] = 5700
    elif station == 'augsburg':
        answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/Augsburg/Solar/10MinSolar.txt"
        answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/Augsburg/Temperatur/10MinTemp.txt"
        answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/Augsburg/Wind/10MinWind.txt"
        answer_dict['coords'] = (48.4253, 10.9417)
        answer_dict['height_exp'] = 0.26
        answer_dict['windturbine'] = 'Nordex N149/5.7'
        answer_dict['hub_height'] = 150
        answer_dict['pv_cap'] = 5700
    elif station == 'luedenscheid':
        answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/Lüdenscheid/Solar/10MinSolar.txt"
        answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/Lüdenscheid/Temperatur/10MinTemp.txt"
        answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/Lüdenscheid/Wind/10MinWind.txt"
        answer_dict['coords'] = (51.2452, 7.6425)
        answer_dict['height_exp'] = 0.26
        answer_dict['windturbine'] = 'Nordex N149/5.7'
        answer_dict['hub_height'] = 150
        answer_dict['pv_cap'] = 5700
    elif station == 'waibstadt':
        answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/Waibstadt/Solar/10MinSolar.txt"
        answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/Waibstadt/Temperatur/10MinTemp.txt"
        answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/Waibstadt/Wind/10MinWind.txt"
        answer_dict['coords'] = (49.2943, 8.9053)
        answer_dict['height_exp'] = 0.26
        answer_dict['windturbine'] = 'Nordex N149/5.7'
        answer_dict['hub_height'] = 150
        answer_dict['pv_cap'] = 5700
    elif station == 'werl':
        answer_dict['solar_url'] = "C:/Users/nilsb/Data/Wetterdaten/Werl/Solar/10MinSolar.txt"
        answer_dict['temp_url'] = "C:/Users/nilsb/Data/Wetterdaten/Werl/Temperatur/10MinTemp.txt"
        answer_dict['wind_url'] = "C:/Users/nilsb/Data/Wetterdaten/Werl/Wind/10MinWind.txt"
        answer_dict['coords'] = (51.5763, 7.8879)
        answer_dict['height_exp'] = 0.26
        answer_dict['windturbine'] = 'Nordex N149/5.7'
        answer_dict['hub_height'] = 150
        answer_dict['pv_cap'] = 5700
    else:
        raise ValueError('Wetterstation nicht vorhanden')
    return answer_dict
