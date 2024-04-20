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
        user_city = request.form.get('user_city')
        info = req.get(f'https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={API}&units=metric')
        data = info.json()
        if data['cod'] == 200:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            temp_feels_like = data['main']['feels_like']
            wind_speed = data['wind']['speed']
        else:
            return 'Error with cod' + data['cod']
    return '''

<html>
<head>
  <meta charset="UTF-8">
  <!--<link href="css/main.css" rel="stylesheet">-->
  <style>
  html, body {
      margin:0;
      padding:0;
      height:100vh;
      background-color: #E0FFFF;
  }

  .header {
    margin:0;
    padding:0;
    display: block;
    width: 100%;
    height: 10%;
    background-color:  #E0FFFF;
  }

  .ender {
    margin:0;
    padding:0;
    position:absolute;
    bottom:0;
    width: 100%;
    height: 10%;
    background-color: #E0FFFF;
  }

  .left {
    margin:0;
    padding:0;
    background-color:  #E0FFFF;
    width: 10%;
    height: 80%;
    float:left;

  }

  .right {
    margin:0;
    padding:0;
    background-color:  #E0FFFF;
    width: 10%;
    height: 80%;
    float: right;
  }


  .form {
    position: relative;
    bottom: -25%;
    left: 15%;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 50%;
    height: 30%;
    background-color: #87CEFA;
    max-width: 2560px;
    border-radius: 20px;
  }
  .form_group {
    text-align: center;
    margin: 0 auto;
  }

  #user_city {
    background-color: #ADD8E6;
    border-color: #ADD8E6;
    border-radius: 9px;
    width: 100%;
    height: 25px;
  }

  #button {
    position: relative;
    width: 25%;
    height: 35px;
    border-radius: 12px;
    background-color: #B0C4DE;
    box-shadow: 0 4px 16px #778899;
    border-color: #B0C4DE;
  }
  #news_button {
    position: relative;
    width: 15%;
    height: 25px;
    margin-top: 5px;
    border-radius: 9px;
    background-color: #B0C4DE;
    box-shadow: 0 4px 16px #778899;
    border-color: #B0C4DE;
  }
  </style>
  <title>Главная страница</title>

</head>
<body>
  <form class='header'></form>
  <form class='ender'></form>
  <form class='left'></form>
  <form class='right'></form>

<form action=""
      method="POST"
      class="form">
    <div class='form_group'>
      <h1 class='form_title'>Weather by city name</h1>

    <input
      type="text"
      placeholder="Enter your city"
      name="user_city"
      id="user_city"><br>
    </div>
  </form>
    <form action="https://rdinviter.pythonanywhere.com/weather" method="get"  class='form_group'>
      <button id="button">Показать информацию</button><br>  </form>
    <form action="https://rdinviter.pythonanywhere.com/news" method="get"  class='form_group'>
        <button id="news_button">Новости</button></form>
  </body>
</html>

'''







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






