import discord
from discord.ext import commands
import json
import random
import os
import time

with open('setting.json',mode = 'r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.default()
intents.members = True  
#discord 1.5之更新

bot = commands.Bot(command_prefix="==",intents = intents)

@bot.event #bot有無開啟
async def on_ready():
    print('>> Bot is online <<')


@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded {extension} done.')
@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Un-Loaded {extension} done.')
@bot.command()
async def reload(ctx,extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'Re-Loaded {extension} done.')    


for filename in os.listdir("./cmds"):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')


if __name__ == "__main__":
    bot.run(jdata["TOKEN"])
