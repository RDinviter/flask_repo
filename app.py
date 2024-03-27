from flask import Flask, render_template, request
import requests as req
from json import *
from weather_file_functions import *
# import webbrowser

# webbrowser.open_new('http://127.0.0.1:5000')

API = 'c9ed96787da81c9fac403046e34131d5'

app = Flask(__name__, '/static')


@app.route('/', methods=['post', 'get'])
def index():
    if request.method == 'POST':
        global user_city
        user_city = request.form['user_city']
        # user_city = request.form['user_city'] another way
        info = req.get(f'https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={API}&units=metric')
        data = info.json()
        if data['cod'] == 200:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            temp_feels_like = data['main']['feels_like']
            wind_speed = data['wind']['speed']
            write_weather_information(user_city, temp, temp_feels_like, humidity, wind_speed)

        else:
            write_error(data)

    return render_template('index.html')


@app.route('/weather')
def weather():
    return render_template('temp.html')


@app.route('/about_city')
def show_info_about_city():
    write_information_about_city(user_city)
    return render_template('info_about_city.html')


@app.route('/forecast')
def show_forecast():
    write_weather_forecast(user_city)
    return render_template('weather_forecast.html')


if __name__ == "__main__":
    app.run(debug=True)
