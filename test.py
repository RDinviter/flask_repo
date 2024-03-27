import requests as req


API = 'c9ed96787da81c9fac403046e34131d5'
city_name = 'London'
cnt = 5

all_masses = [[], [], [], [], [], []]

mass_time = []
mass_all_info = []

mass_days = []

info = req.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API}&units=metric')

data = info.json()


for i in range(len(data['list'])):
    mass_time.append(data['list'][i]['dt_txt'])
    mass_all_info.append(data['list'][i]['main'])

forecast_dict = dict(zip(mass_time, mass_all_info))

for i in range(0, len(forecast_dict) - 1):
    if mass_time[i][8:10] != mass_time[i + 1][8:10]:
        mass_days.append(i)


j = 0
all_masses[0].append(f'<form class="first_weather_form"><div class="first_div"><h2 id="first_title">Прогноз на {mass_time[mass_days[0]][:10]}:</h2>')
all_masses[1].append(f'<form class="second_weather_form"> <div class="second_div"><h2 id="second_title">Прогноз на {mass_time[mass_days[1]][:10]}</h2>')
all_masses[2].append(f'<form class="third_weather_form"><div class="third_div"><h2 id="third_title">Прогноз на {mass_time[mass_days[2]][:10]}</h2>')
all_masses[3].append(f'<form class="fourth_weather_form"><div class="fourth_div"><h2 id="fourth_title">Прогноз на {mass_time[mass_days[3]][:10]}</h2>')

for i in range(0, len(forecast_dict) - 1):
    all_masses[j].append(f'''<b>{mass_time[i][11:19]}:</b><br>
       Температура: {(forecast_dict[mass_time[i]]['temp'])}<br>
       Ощущается как: {(forecast_dict[mass_time[i]]['feels_like'])}<br>
       Влажность: {(forecast_dict[mass_time[i]]['humidity'])}%''')
    if mass_time[i][8:10] != mass_time[i + 1][8:10]:
        j += 1


# print(mass_time[1][11:13])

with open('test.html', 'w', encoding='utf-8') as temp_file:
    temp_file.write(f"""
    <html>
    <head>
        <title>Weather</title>
        <meta charset='UTF-8'>
        <link rel="stylesheet" href="../static/css/temp_styles.css">
    </head>
    <body>""")


with open('test.html', 'a+', encoding='utf-8') as file:
    for i in all_masses[0]:
        file.write(i + '<br>')
    file.write('</div></form>')


with open('test.html', 'a+', encoding='utf-8') as file:
    for i in all_masses[1]:
        file.write(i + '<br>')
    file.write('</div></form>')


with open('test.html', 'a+', encoding='utf-8') as file:
    for i in all_masses[2]:
        file.write(i + '<br>')
    file.write('</div></form>')


with open('test.html', 'a+', encoding='utf-8') as file:
    for i in all_masses[3]:
        file.write(i + '<br>')
    file.write('</div></form></body></html>')

print(data)