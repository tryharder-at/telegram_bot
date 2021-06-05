import requests
from settings import weather_api_key
from geocoder import get_coordinates
cond={'clear':'ясно','partly-cloudy': 'малооблачно','cloudy':'облачно с прояснениями',
            'overcast':'пасмурно',
            'partly-cloudy-and-light-rain':'небольшой дождь',
            'partly-cloudy-and-rain':'дождь',
           'overcast-and-rain':'сильный дождь',
           'overcast-thunderstorms-with-rain':'сильный дождь, гроза',
      'cloudy-and-light-rain':'облачно, небольшой дождь'
           }
# clear — ясно.
# partly-cloudy — малооблачно.
# cloudy — облачно с прояснениями.
# overcast — пасмурно.
# partly-cloudy-and-light-rain — небольшой дождь.
# partly-cloudy-and-rain — дождь.
# overcast-and-rain — сильный дождь.
# overcast-thunderstorms-with-rain — сильный дождь, гроза.
# cloudy-and-light-rain — небольшой дождь.
# overcast-and-light-rain — небольшой дождь.
# cloudy-and-rain — дождь.
# overcast-and-wet-snow — дождь со снегом.
# partly-cloudy-and-light-snow — небольшой снег.
# partly-cloudy-and-snow — снег.
# overcast-and-snow — снегопад.
# cloudy-and-light-snow — небольшой снег.
# overcast-and-light-snow — небольшой снег.
# cloudy-and-snow — снег.

headers = {"X-Yandex-API-Key": weather_api_key}

# translation = requests.get('https://api.weather.yandex.ru/v1/translations?lang=ru_RU', headers=headers).json()


def get_weather(place):
    api_server = "https://api.weather.yandex.ru/v2/forecast?"

    coord = get_coordinates(place)

    forecast = []

    params = {
        'lat': coord[1],
        'lon': coord[0],
        'lang': 'ru_RU'
    }

    response = requests.get(api_server, headers=headers, params=params)

    json_response = response.json()
    now_weather = json_response['fact']
    future_weather = json_response['forecasts']
    print(future_weather)
    forecast.append({'temp': now_weather['temp'],
                     'feels_like': now_weather['feels_like'],
                     # 'condition': translation[now_weather['condition']],
                     'condition': cond[now_weather['condition']],
                     'date': 'сегодня'})

    for i in range(1, 4):
        _weather = {}
        _weather['date'] = future_weather[i]['date']
        _weather['temp'] = future_weather[i]['parts']['day']['temp_avg']
        _weather['feels_like'] = future_weather[i]['parts']['day']['feels_like']
        # _weather['condition'] = translation[future_weather[i]['parts']['day']['condition']]
        _weather['condition'] = cond[future_weather[i]['parts']['day']['condition']]
        forecast.append(_weather.copy())

    return forecast

# str='Москва'
#
# weather = get_weather(str)
# print((weather))
