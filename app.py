from flask import Flask, render_template, request
import requests as req
from weather_file_functions import WeatherInfoByCity, write_weather_forecast, get_news
import wikipedia as wiki
import textwrap
wrapper = textwrap.TextWrapper(width=20)


API = 'c9ed96787da81c9fac403046e34131d5'
news_api_key = 'd252fc39f3614de0a93db12805dc04ed'



moscow = WeatherInfoByCity('Moscow')
london = WeatherInfoByCity('London')
abu_dabi = WeatherInfoByCity('Абу-Даби')
berlin = WeatherInfoByCity('Berlin')

app = Flask(__name__, '/static')

@app.route('/', methods=['post', 'get'])
def index():
    if request.method == 'POST':
        global user_city
        global temp
        global humidity
        global wind_speed
        global temp_feels_like
        user_city = request.form['user_city']
        info = req.get(f'https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={API}&units=metric')
        data = info.json()
        if data['cod'] == 200:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            temp_feels_like = data['main']['feels_like']
            wind_speed = data['wind']['speed']
        else:
            return 'Error with cod' + data['cod']
    return """
<html>
<head>
  <meta charset="UTF-8">
  <title>Главная страница</title>
  <style>

body {
  display: flex;
  background-color: #E0FFFF;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.form_button {
  position: relative;
  bottom: -30px;
  right: 365px;
}

.form {
  width: 500px;
  height: 200px;
  padding: 32px;
  border-radius: 20px;
  box-shadow: 0 4px 16px #ccc;
  background-color: #87CEFA;
}

.form_title {
  position: relative;
  left: 85;
}

#user_city {
  width: 250px;
  position: relative;
  left: 115;
}

#user_city {
  width: 250px;
  position: relative;
  left: 115;
  display: block;
  background-color: #ADD8E6;
  border-color: #ADD8E6;
  border-radius: 5px;
}

#button {
  position: relative;
  background-color: #B0C4DE;
  left: -250px;
  width: 170px;
  height: 35px;
  border-radius: 9px;
  box-shadow: 0 4px 16px #778899;
  border-color: #B0C4DE;
}

.moscow_weather {
  position: relative;
  width: 240px;
  height: 310px;
  left: -900px;
  background-color: #87CEFA;
  bottom: -163px;
  border-radius: 20px;
  box-shadow: 0 4px 16px #ccc;
}
.moscow_title {
  position: relative;
  left: 40px;
  bottom: -10px;
}
.moscow_information {
  position: relative;
  left: 30px;
}

.london_weather {
  position: relative;
  width: 240px;
  height: 310px;
  left: -550px;
  background-color: #87CEFA;
  bottom: 168px;
  border-radius: 20px;
  box-shadow: 0 4px 16px #ccc;
}

.london_title {
  position: relative;
  left: 40px;
  bottom: -10px;
}
.london_information {
  position: relative;
  left: 30px;
}

.abu_dabi_weather {
  position: relative;
  width: 240px;
  height: 310px;
  left: -200px;
  background-color: #87CEFA;
  bottom: 500px;
  border-radius: 20px;
  box-shadow: 0 4px 16px #ccc;
}

.abu_dabi_title {
  position: relative;
  left: 40px;
  bottom: -10px;
}
.abu_dabi_information {
  position: relative;
  left: 30px;
}

.berlin_weather {
  position: relative;
  width: 240px;
  height: 310px;
  left: 150px;
  background-color: #87CEFA;
  bottom: 830px;
  border-radius: 20px;
  box-shadow: 0 4px 16px #ccc;
}

.berlin_title {
  position: relative;
  left: 40px;
  bottom: -10px;
}
.berlin_information {
  position: relative;
  left: 30px;
}

#news_button {
  position: relative;
  background-color: #B0C4DE;
  left: -785px;
  bottom: -70px;
  width: 170px;
  height: 35px;
  border-radius: 9px;
  box-shadow: 0 4px 16px #778899;
  border-color: #B0C4DE;
}
  </style>
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
      <h2 class='moscow_information'>Temperatue: """ + str(moscow.temp) + """</h2>
      <h2 class='moscow_information'>Feels like: """ + str(moscow.temp_feels_like) + """</h2>
      <h2 class='moscow_information'>Humidity: """ + str(moscow.humidity) + """</h2>
      <h2 class='moscow_information'>Wind speed:""" +  str(moscow.wind_speed) + """</h2></div>

    <div class='london_weather'>
      <h1 class='london_title'>Weather in London</h1>
      <h2 class='london_information'>Temperatue: """ + str(london.temp) + """</h2>
      <h2 class='london_information'>Feels like: """ + str(london.temp_feels_like) + """</h2>
      <h2 class='london_information'>Humidity: """ + str(london.humidity) + """</h2>
      <h2 class='london_information'>Wind speed: """ + str(london.wind_speed) + """</h2></div>
    <div class='abu_dabi_weather'>
        <h1 class='abu_dabi_title'>Weather in<br>
           Абу-Даби</h1>
        <h2 class='abu_dabi_information'>Temperatue: """ + str(abu_dabi.temp) + """</h2>
        <h2 class='abu_dabi_information'>Feels like: """+ str(abu_dabi.temp_feels_like) + """</h2>
        <h2 class='abu_dabi_information'>Humidity: """ + str(abu_dabi.humidity) + """</h2>
        <h2 class='abu_dabi_information'>Wind speed: """ + str(abu_dabi.wind_speed) + """</h2></div>
    <div class='berlin_weather'>
        <h1 class='berlin_title'>Weather in Берлин</h1>
        <h2 class='berlin_information'>Temperatue: """ + str(berlin.temp) + """</h2>
        <h2 class='berlin_information'>Feels like: """ + str(berlin.temp_feels_like) + """</h2>
        <h2 class='berlin_information'>Humidity: """ + str(berlin.humidity) + """</h2>
        <h2 class='berlin_information'>Wind speed: """ + str(berlin.wind_speed) + """</h2></div>
  </form>
  <form action="https://rdinviter.pythonanywhere.com/weather" method="get"  class='form_button'>
    <button id="button">Показать информацию</button>
  </form>
    <form action="https://rdinviter.pythonanywhere.com/news" method="get"  class='news_button'>
      <button id="news_button">Новости</button>
  </form>
    </body>
</html>"""


@app.route('/weather')
def weather():
    return """
    <html>
    <head>
        <title>Weather</title>
        <meta charset='UTF-8'>
        <style>
        body {
  display: flex;
  background-color: #E0FFFF;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.form {
  width: 500px;
  height: 250px;
  padding: 32px;
  border-radius: 20px;
  box-shadow: 0 4px 16px #ccc;
  background-color: #87CEFA;
}

.weather_title {
  display: flex;
  justify-content: center;
}

.weather_information {
  display: flex;
  justify-content: center;
}

#info_button {
  position: relative;
  background-color: #B0C4DE;
  width: 170px;
  height: 35px;
  border-radius: 9px;
  box-shadow: 0 4px 16px #778899;
  border-color: #B0C4DE;
  left: -260px;
  bottom: -180px;
}

#forecast_button {
  position: relative;
  background-color: #B0C4DE;
  width: 170px;
  height: 35px;
  border-radius: 9px;
  box-shadow: 0 4px 16px #778899;
  border-color: #B0C4DE;
  left: -620px;
  bottom: -180px;
}
</style>
</head>
<body>
<form class='form'>
<div>
            <h1 class='weather_title'>Weather in""" + ' ' + user_city + """</h1>
            <h2 class='weather_information'>Temperatue: """ + str(temp) + """</h2>
            <h2 class='weather_information'>Feels like: """ + str(temp_feels_like) + """</h2>
            <h2 class='weather_information'>Humidity: """ + str(humidity) + """</h2>
            <h2 class='weather_information'>Wind speed: """ + str(wind_speed) + """</h2>
          </div>
        </form>
        <form class='info_button' action="https://rdinviter.pythonanywhere.com/about_city" method="get">
          <button id='info_button'>Информация о городе</button>
        </form>
        <form class='forecast_button' action="https://rdinviter.pythonanywhere.com/forecast" method="get">
          <button id='forecast_button'>Прогноз погоды</button>
        </form>
    </body>
    </html>
    """


@app.route('/about_city')
def show_info_about_city():
    try:
        city_wiki_page = wiki.summary(user_city, sentences=10)
        city_wiki_page = wrapper.fill(city_wiki_page)
    except:
        city_wiki_page = "Error"
    return """<html>
    <head>
      <meta charset="UTF-8">
      <title>information</title>
      <style>

body {
  display: flex;
  background-color: #E0FFFF;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.form {
  width: 700px;
  height: 500px;
  padding: 32px;
  border-radius: 20px;
  box-shadow: 0 4px 16px #ccc;
  background-color: #87CEFA;
}

.form_title {
  display: flex;
  justify-content: center;
}

.weather_information {
  display: flex;
  justify-content: center;
}

p {
font-size: 20px;
}

      </style>

    </head>
    <body>
      <form action=""
            method="POST"
            class="form">

        <h1 class='form_title'>Some information about """  + user_city + """</h1>
        <p>""" + city_wiki_page + """</p>
      </form>
        </body>
    </html>"""


@app.route('/forecast')
def show_forecast():
    return '<h1 font-size="50">Страница в разработке :(</h1>'


@app.route('/news')
def show_news():
    get_news(news_api_key)
    return render_template('news_page.html')
