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


def write_weather_information(user_city, temp, temp_feels_like, humidity, wind_speed):
    with open('templates/temp.html', 'w', encoding='utf-8') as temp_file:
        temp_file.write(f"""
    <html>
    <head>
        <title>Weather</title>
        <meta charset='UTF-8'>
        <link rel="stylesheet" href="../static/css/temp_styles.css">
    </head>
    <body>
        <form class='form'>
          <div>
            <h1 class='weather_title'>Weather in {user_city}</h1>
            <h2 class='weather_information'>Temperatue: {temp}</h2>
            <h2 class='weather_information'>Feels like: {temp_feels_like}</h2>
            <h2 class='weather_information'>Humidity: {humidity}</h2>
            <h2 class='weather_information'>Wind speed: {wind_speed}</h2>
          </div>
        </form>
        <form class='info_button' action="http://127.0.0.1:5000/about_city" method="get">
          <button id='info_button'>Информация о городе</button>
        </form>
        <form class='forecast_button' action="http://127.0.0.1:5000/forecast" method="get">
          <button id='forecast_button'>Прогноз погоды</button>
        </form>
    </body>
    </html>
    """)


def write_error(data):
    with open('templates/temp.html', 'w', encoding='utf-8') as temp_file:
        temp_file.write(f"""
                   <html>
                   <head>
                       <title>Weather</title>
                       <meta charset='UTF-8'>
                       <link rel="stylesheet" href="../static/css/temp_styles.css">
                   </head>
                   <body>
                       <form class='form'>
                       <h1>Error with cod {data['cod']}</h1>
                       <h2>Возможно, вы неправильно ввели город</h2>
                       <h2>Попробуйте еще раз</h2>
                       </form>
                   </body>
                   </html>
                   """)


def write_information_about_city(user_city):
    try:
        city_wiki_page = wiki.summary(user_city, sentences=10)
        city_wiki_page = wrapper.fill(city_wiki_page)
    except:
        city_wiki_page = "Error"
    with open('templates/info_about_city.html', 'w', encoding='utf-8') as info_file:
        info_file.write(f"""<html>
    <head>
      <meta charset="UTF-8">
      <title>information</title>
      <link rel="stylesheet" href="../static/css/city_info_styles.css">

    </head>
    <body>
      <form action=""
            method="POST"
            class="form">

        <h1 class='form_title'>Some information about {user_city}</h1>
        <p>{city_wiki_page}</p>
      </form>
        </body>
    </html>""")


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

    with open('templates/weather_forecast.html', 'w', encoding='utf-8') as file:
        file.write(f"""
        <html>
        <head>
            <title>Weather</title>
            <meta charset='UTF-8'>
            <link rel="stylesheet" href="../static/css/weather_forecast_styles.css">
        </head>
        <body>""")

    with open('templates/weather_forecast.html', 'a+', encoding='utf-8') as file:
        for i in all_masses[0]:
            file.write(i + '<br>')
        file.write('</div></form>')

    with open('templates/weather_forecast.html', 'a+', encoding='utf-8') as file:
        for i in all_masses[1]:
            file.write(i + '<br>')
        file.write('</div></form>')

    with open('templates/weather_forecast.html', 'a+', encoding='utf-8') as file:
        for i in all_masses[2]:
            file.write(i + '<br>')
        file.write('</div></form>')

    with open('templates/weather_forecast.html', 'a+', encoding='utf-8') as file:
        for i in all_masses[3]:
            file.write(i + '<br>')
        file.write('</div></form></body></html>')


def write_index_capitals_info():
    moscow = WeatherInfoByCity('Moscow')
    london = WeatherInfoByCity('London')
    abu_dabi = WeatherInfoByCity('Абу-Даби')
    berlin = WeatherInfoByCity('Berlin')

    with open('templates/index.html', 'w', encoding='utf-8') as index_file:
        index_file.write(f"""
<html>
<head>
  <meta charset="UTF-8">
  <title>Главная страница</title>
  <link rel="stylesheet" href="../static/css/main.css">
</head>
<body>
  <form action=""
        method="POST"
        class="form">

    <h1 class='form_title'>Weather by city name</h1>
    <div class='form_group'>
      <input
        type="text"
        placeholder="Enter your city"
        name="user_city"
        id="user_city">
    </div>
  </form>
  <form>
    <div class='moscow_weather'>
      <h1 class='moscow_title'>Weather in Moscow</h1>
      <h2 class='moscow_information'>Temperatue: {moscow.temp}</h2>
      <h2 class='moscow_information'>Feels like: {moscow.temp_feels_like}</h2>
      <h2 class='moscow_information'>Humidity: {moscow.humidity}</h2>
      <h2 class='moscow_information'>Wind speed: {moscow.wind_speed}</h2></div>

    <div class='london_weather'>
      <h1 class='london_title'>Weather in London</h1>
      <h2 class='london_information'>Temperatue: {london.temp}</h2>
      <h2 class='london_information'>Feels like: {london.temp_feels_like}</h2>
      <h2 class='london_information'>Humidity: {london.humidity}</h2>
      <h2 class='london_information'>Wind speed: {london.wind_speed}</h2></div>
    <div class='abu_dabi_weather'>
        <h1 class='abu_dabi_title'>Weather in<br>
           Абу-Даби</h1>
        <h2 class='abu_dabi_information'>Temperatue: {abu_dabi.temp}</h2>
        <h2 class='abu_dabi_information'>Feels like: {abu_dabi.temp_feels_like}</h2>
        <h2 class='abu_dabi_information'>Humidity: {abu_dabi.humidity}</h2>
        <h2 class='abu_dabi_information'>Wind speed: {abu_dabi.wind_speed}</h2></div>
    <div class='berlin_weather'>
        <h1 class='berlin_title'>Weather in Берлин</h1>
        <h2 class='berlin_information'>Temperatue: {berlin.temp}</h2>
        <h2 class='berlin_information'>Feels like: {berlin.temp_feels_like}</h2>
        <h2 class='berlin_information'>Humidity: {berlin.humidity}</h2>
        <h2 class='berlin_information'>Wind speed: {berlin.wind_speed}</h2></div>
  </form>
  <form action="http://127.0.0.1:5000/weather" method="get"  class='form_button'>
    <button id="button">Показать информацию</button>
  </form>
    <form action="http://127.0.0.1:5000/news" method="get"  class='news_button'>
      <button id="news_button">Новости</button>
  </form>
    </body>
</html>
""")


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
        with open('templates/news_page.html', 'w', encoding='utf=8') as out_file:
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
