import wikipedia as wiki
import textwrap
import requests as req
wrapper = textwrap.TextWrapper(width=20)
wiki.set_lang('ru')

API = 'c9ed96787da81c9fac403046e34131d5'

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

    cnt = 5

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
        f'<form class="first_weather_form"><div class="first_div"><h2 id="first_title">Прогноз на {mass_time[mass_days[0]][:10]}:</h2>')
    all_masses[1].append(
        f'<form class="second_weather_form"> <div class="second_div"><h2 id="second_title">Прогноз на {mass_time[mass_days[1]][:10]}</h2>')
    all_masses[2].append(
        f'<form class="third_weather_form"><div class="third_div"><h2 id="third_title">Прогноз на {mass_time[mass_days[2]][:10]}</h2>')
    all_masses[3].append(
        f'<form class="fourth_weather_form"><div class="fourth_div"><h2 id="fourth_title">Прогноз на {mass_time[mass_days[3]][:10]}</h2>')

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

    moscow_info = req.get(f'https://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={API}&units=metric')
    moscow_data = moscow_info.json()
    moscow_temp = moscow_data['main']['temp']
    moscow_humidity = moscow_data['main']['humidity']
    moscow_temp_feels_like = moscow_data['main']['feels_like']
    moscow_wind_speed = moscow_data['wind']['speed']

    london_info = req.get(f'https://api.openweathermap.org/data/2.5/weather?q=London&appid={API}&units=metric')
    london_data = london_info.json()
    london_temp = london_data['main']['temp']
    london_humidity = london_data['main']['humidity']
    london_temp_feels_like = london_data['main']['feels_like']
    london_wind_speed = london_data['wind']['speed']

    abu_dabi_info = req.get(f'https://api.openweathermap.org/data/2.5/weather?q=Абу-Даби&appid={API}&units=metric')
    abu_dabi_data = abu_dabi_info.json()
    abu_dabi_temp = abu_dabi_data['main']['temp']
    abu_dabi_humidity = abu_dabi_data['main']['humidity']
    abu_dabi_temp_feels_like = abu_dabi_data['main']['feels_like']
    abu_dabi_wind_speed = abu_dabi_data['wind']['speed']

    berlin_info = req.get(f'https://api.openweathermap.org/data/2.5/weather?q=Абу-Даби&appid={API}&units=metric')
    berlin_data = berlin_info.json()
    berlin_temp = berlin_data['main']['temp']
    berlin_humidity = berlin_data['main']['humidity']
    berlin_temp_feels_like = berlin_data['main']['feels_like']
    berlin_wind_speed = berlin_data['wind']['speed']

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
      <h2 class='moscow_information'>Temperatue: {moscow_temp}</h2>
      <h2 class='moscow_information'>Feels like: {moscow_temp_feels_like}</h2>
      <h2 class='moscow_information'>Humidity: {moscow_humidity}</h2>
      <h2 class='moscow_information'>Wind speed: {moscow_wind_speed}</h2></div>

    <div class='london_weather'>
      <h1 class='london_title'>Weather in London</h1>
      <h2 class='london_information'>Temperatue: {london_temp}</h2>
      <h2 class='london_information'>Feels like: {london_temp_feels_like}</h2>
      <h2 class='london_information'>Humidity: {london_humidity}</h2>
      <h2 class='london_information'>Wind speed: {london_wind_speed}</h2></div>
    <div class='abu_dabi_weather'>
        <h1 class='abu_dabi_title'>Weather in<br>
           Абу-Даби</h1>
        <h2 class='abu_dabi_information'>Temperatue: {abu_dabi_temp}</h2>
        <h2 class='abu_dabi_information'>Feels like: {abu_dabi_temp_feels_like}</h2>
        <h2 class='abu_dabi_information'>Humidity: {abu_dabi_humidity}</h2>
        <h2 class='abu_dabi_information'>Wind speed: {abu_dabi_wind_speed}</h2></div>
    <div class='berlin_weather'>
        <h1 class='berlin_title'>Weather in Берлин</h1>
        <h2 class='berlin_information'>Temperatue: {berlin_temp}</h2>
        <h2 class='berlin_information'>Feels like: {berlin_temp_feels_like}</h2>
        <h2 class='berlin_information'>Humidity: {berlin_humidity}</h2>
        <h2 class='berlin_information'>Wind speed: {berlin_wind_speed}</h2></div>
  </form>
  <form action="http://127.0.0.1:5000/weather" method="get"  class='form_button'>
    <button id="button">Показать информацию</button>
  </form>

    </body>
</html>
""")
