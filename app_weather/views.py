from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}


def current_weather(lat, lon):
    """
    Описание функции, входных и выходных переменных
    Получает широту и долготу в градусах
    Возвращает данные о погоде
    """
    token = '3971c94a-1ad6-4a2a-95c3-4468549ecf3a'  # Вставить ваш токен
    url = f"https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}"
    headers = {"X-Yandex-API-Key": f"{token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    result = {
        'temp': data['fact']['temp'],
        'feels_like_temp': data['fact']['feels_like'],
        'pressure': data['fact']['pressure_mm'],
        'humidity': data['fact']['humidity'],
        'wind_speed': data['fact']['wind_speed'],
        'wind_gust': data['fact']['wind_gust'],
    }
    return result


def weather_view(request):
    if request.method == "GET":
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        if lat and lon:
            data = current_weather(lat=lat, lon=lon)
        else:
            data = current_weather(59.93, 30.31)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})

# if __name__ == "__main__":
#     print(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга