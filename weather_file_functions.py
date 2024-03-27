import wikipedia as wiki
import textwrap
import requests as req
wrapper = textwrap.TextWrapper(width=20)
wiki.set_lang('ru')


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
                       <form class='info_button' action="http://127.0.0.1:5000/about_city" method="get">
                         <button id='info_button'>Информация о городе</button>
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
    API = 'c9ed96787da81c9fac403046e34131d5'
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
