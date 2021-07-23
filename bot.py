# bot.py
# bot.py
import os
import random
import discord
import math
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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

bot.run(TOKEN)