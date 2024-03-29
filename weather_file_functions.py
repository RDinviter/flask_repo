import wikipedia as wiki
import textwrap
import requests as req
wrapper = textwrap.TextWrapper(width=20)
wiki.set_lang('ru')

API = 'c9ed96787da81c9fac403046e34131d5'
news_api_key = 'd252fc39f3614de0a93db12805dc04ed'


class WeatherInfoByCity:
    def __init__(self, city_name):
        self.info = req.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API}&units=metric')
        self.data = self.info.json()
        self.temp = self.data['main']['temp']
        self.humidity = self.data['main']['humidity']
        self.temp_feels_like = self.data['main']['feels_like']
        self.wind_speed = self.data['wind']['speed']



def write_weather_forecast(user_city):

    all_masses = [[], [], [], [], [], []]

    mass_time = []
    mass_all_info = []

    mass_days = []

    info = req.get(f'https://api.openweathermap.org/data/2.5/forecast?q={user_city}&appid={API}&units=metric')

    data = info.json()

    for i in range(len(data['list'])):
        mass_time.append(data['list'][i]['dt_txt'])
        mass_all_info.append(data['list'][i]['main'])

    forecast_dict = dict(zip(mass_time, mass_all_info))

    for i in range(0, len(forecast_dict) - 1):
        if mass_time[i][8:10] != mass_time[i + 1][8:10]:
            mass_days.append(i)

    j = 0
    all_masses[0].append(
        f'<form class="first_weather_form"><div class="first_div"><h2 id="first_title">'
        f'Прогноз на {mass_time[mass_days[0]][:10]}:</h2>')
    all_masses[1].append(
        f'<form class="second_weather_form"> <div class="second_div"><h2 id="second_title">'
        f'Прогноз на {mass_time[mass_days[1]][:10]}</h2>')
    all_masses[2].append(
        f'<form class="third_weather_form"><div class="third_div"><h2 id="third_title">'
        f'Прогноз на {mass_time[mass_days[2]][:10]}</h2>')
    all_masses[3].append(
        f'<form class="fourth_weather_form"><div class="fourth_div"><h2 id="fourth_title">'
        f'Прогноз на {mass_time[mass_days[3]][:10]}</h2>')

    for i in range(0, len(forecast_dict) - 1):
        all_masses[j].append(f'''<b>{mass_time[i][11:19]}:</b><br>
           Температура: {(forecast_dict[mass_time[i]]['temp'])}<br>
           Ощущается как: {(forecast_dict[mass_time[i]]['feels_like'])}<br>
           Влажность: {(forecast_dict[mass_time[i]]['humidity'])}%''')
        if mass_time[i][8:10] != mass_time[i + 1][8:10]:
            j += 1

    with open('mysite/templates/weather_forecast.html', 'w', encoding='utf-8') as file:
        file.write(f"""
        <html>
        <head>
            <title>Weather</title>
            <meta charset='UTF-8'>
            <link rel="stylesheet" href="../static/css/weather_forecast_styles.css">
        </head>
        <body>""")

    with open('mysite/templates/weather_forecast.html', 'a+', encoding='utf-8') as file:
        for i in all_masses[0]:
            file.write(i + '<br>')
        file.write('</div></form>')

    with open('mysite/templates/weather_forecast.html', 'a+', encoding='utf-8') as file:
        for i in all_masses[1]:
            file.write(i + '<br>')
        file.write('</div></form>')

    with open('mysite/templates/weather_forecast.html', 'a+', encoding='utf-8') as file:
        for i in all_masses[2]:
            file.write(i + '<br>')
        file.write('</div></form>')

    with open('mysite/templates/weather_forecast.html', 'a+', encoding='utf-8') as file:
        for i in all_masses[3]:
            file.write(i + '<br>')
        file.write('</div></form></body></html>')





def get_news(api_key):
    url = "http://newsapi.org/v2/top-headlines"
    params = {
        'country': 'us',  # Измените страну при необходимости
        'apiKey': api_key
    }

    response = req.get(url, params=params)
    data = response.json()
    print(data)

    if data['status'] == 'ok':
        articles = data['articles']
        count = 0
        with open('mysite/templates/news_page.html', 'w', encoding='utf=8') as out_file:
            out_file.write("""<html>
<head>
  <meta charset="UTF-8">
  <title>Главная страница</title>
  <link rel="stylesheet" href="../static/css/news_page_styles.css">
</head>
<body>""")

            for idx, article in enumerate(articles, start=1):
                out_file.write(f'<form class="form_news" action="{article["url"]}" method="get">\n')
                out_file.write(f"""<h4 class='news_titles'>{idx}. {article['title']}</h4>
                                    <button class='form_buttons'>Read more</button>""")
                out_file.write(f'</form>')
                count += 1
                # out_file.write(article['url'])
                out_file.write('\n\n')
            out_file.write("</body></html>")
    else:
        with open('templates/news_page.html', 'w', encoding='utf=8') as out_file:
            out_file.write("Произошла ошибка при получении новостей")

