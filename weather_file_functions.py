import wikipedia as wiki
import textwrap
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
