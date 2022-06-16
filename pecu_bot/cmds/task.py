from ast import If
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json,asyncio,datetime

class Task(Cog_Extension):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.counter = 0

        async def interval(): #bot在背景不斷運行
            await self.bot.wait_until_ready() #bot開啟後
            self.channel = self.bot.get_channel(961655650478354443)
            while not self.bot.is_closed():
                #await self.channel.send('嗨 我還在執行')
                await asyncio.sleep(1800)
        self.bg_task = self.bot.loop.create_task(interval())
                   
    
    @commands.command()
    async def set_channel(self,ctx,channel:int):
        self.channel = self.bot.get_channel(channel)
        await ctx.send(f'將訊息傳送到別的頻道(ID):{self.channel.mention}')


def setup(bot):
    bot.add_cog(Task(bot))