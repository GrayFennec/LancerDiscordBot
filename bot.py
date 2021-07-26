# bot.py
import os
import random
import discord
import math
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WEATHER_KEY = os.getenv('WEATHER_KEY')
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='roll', help='Rolls a skill check')
async def roll(ctx, accuracy_difficulty: int, modifier: int):
    roll = random.randint(1,20)
    response = [
        'Base roll: ' + str(roll)
        ]
    if accuracy_difficulty != 0:
        acc_dif_text = 'Accuracy' if accuracy_difficulty > 0 else 'Difficulty'
        acc_dif_rolls = random.sample(range(1,6), abs(accuracy_difficulty))
        acc_dif_mod = int(max(acc_dif_rolls)*math.copysign(1, accuracy_difficulty))
        response += [
            acc_dif_text + ' rolls: ' + str(acc_dif_rolls),
            acc_dif_text + ' modifier: {0:+}'.format(acc_dif_mod),
        ]
    else:
        acc_dif_mod = 0
    if modifier != 0:
        response += [
            'Other modifiers: {0:+}'.format(modifier)
        ]
    total = int(roll + acc_dif_mod + modifier)
    response += [
        'Total: ' + str(total)
    ]
    await ctx.send('\n'.join(response))

@bot.command(name='weather', help='Gets the weather of one of the habitable moons.\nCurrently supported: Ari, Bay, Cole, Drop')
async def weather(ctx, moon_name):
    moon_city_dictionary = {
        'Ari': 'Riyadh',
        'Bay': 'San Francisco',
        'Cole': 'Svalbard',
        'Drop': 'Singapore',
    }
    try:
        city_name = moon_city_dictionary[moon_name]
    except KeyError:
        await ctx.send('Error: Unsupported moon name.')
        return
    param_set = {'key':WEATHER_KEY,'q':city_name,'aqi':'no'}
    response = requests.get('http://api.weatherapi.com/v1/current.json', params = param_set)
    weather_data = response.json()['current']
    weather_text = [
        '__' + moon_name + ' weather__',
        weather_data['condition']['text'],
        'Temperature: ' + str(weather_data['temp_f']) + '°F',
        'Precipitation: ' + str(weather_data['precip_in']) + 'in',
        'Humidity: ' + str(weather_data['humidity']) + '%',
        'Wind: ' + str(weather_data['wind_mph']) + ' mph ' + weather_data['wind_dir'],
        'Air Pressure: ' + str(weather_data['pressure_in']) + ' in',
        'Cloud Cover: ' + str(weather_data['cloud']) + '%'
    ]
    await ctx.send('\n'.join(weather_text))
bot.run(TOKEN)