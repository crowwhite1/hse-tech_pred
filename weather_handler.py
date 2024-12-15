import json
from urllib import parse, request
import database

API_TOKEN = 'rAA7pMc3dAMAkKRlT6AEmcZvUgNGWGyv'
lang = 'ru-ru'


def get_weather(lat, lon, user):
    """Получение текущей погоды"""
    location_code = get_location_code(lat, lon, user)
    url_current = f'http://dataservice.accuweather.com/currentconditions/v1/{location_code}?apikey={API_TOKEN}&language={lang}'
    with request.urlopen(url_current) as response:
        current_weather = json.loads(response.read().decode())[0]
    return get_response_for_current(current_weather)


def get_response_for_current(current_weather):
    """Генерация ответа для текущей погоды"""
    response = f"Текущая погода: {current_weather['WeatherText']}\n"
    response += f'Осадки: {current_weather['PrecipitationType']}' if current_weather['HasPrecipitation'] else ""
    response += f'Температура: {current_weather['Temperature']['Metric']['Value']}'
    return response


def get_location_code(lat, lon, user):
    """Получение кода местоположения"""
    url_loc = f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={API_TOKEN}&q={lat},{lon}&language={lang}'
    with request.urlopen(url_loc) as response:
        code = json.loads(response.read().decode())['Key']
        database.update_user_geo(user[0], code)
    return code


def get_weather_for_day(lat, lon, user):
    """Получение погоды на день"""
    location_code = get_location_code(lat, lon, user)
    url_tomorrow = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_code}?apikey={API_TOKEN}&language={lang}&metric=True'
    with request.urlopen(url_tomorrow) as response:
        tomorrow_weather = json.loads(response.read().decode())['DailyForecasts'][0]
    return get_response_for_day(tomorrow_weather)


def get_response_for_day(tomorrow_weather):
    """Генерация ответа для погоды на день"""
    response = 'Погода на сегодня:\n'
    response += f"Температура:\nот {tomorrow_weather['Temperature']['Minimum']['Value']} до {tomorrow_weather['Temperature']['Maximum']['Value']}\n"
    response += f'Днём: {tomorrow_weather['Day']['IconPhrase']}\n'
    response += f'Ночью: {tomorrow_weather['Night']['IconPhrase']}\n'
    response += f'Подробности: {tomorrow_weather['Link']}'
    return response


def get_weather_for_day_by_code(location_code):
    """Получение погоды для рассылки"""
    url_tomorrow = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_code}?apikey={API_TOKEN}&language={lang}&metric=True'
    with request.urlopen(url_tomorrow) as response:
        tomorrow_weather = json.loads(response.read().decode())['DailyForecasts'][0]
    return get_response_for_day(tomorrow_weather)
