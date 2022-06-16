from sqlite3 import Timestamp
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import datetime
import random

class Main(Cog_Extension):

    @commands.command() #機器人之延遲(秒→毫秒→四捨五入)
    async def ping(self,ctx): #ctx=上下文    
        await ctx.send(f'{round(self.bot.latency*1000)}(ms)')

    @commands.command() #複誦訊息
    async def sayd(self,ctx,*,msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command() #刪除N筆訊息
    async def clean(self,ctx,num:int):
        await ctx.channel.purge(limit = num+1)
       

    @commands.command() #上線成員分組
    async def rand_squad(self,ctx):
        online = []
        for member in ctx.guild.members:
            print(member.status)
            if str(member.status) == 'offline': #and member.bot==False
                online.append(member.name)
         #↗程式有問題，狀態都呈現offline且成員名單不為該頻道成員，其餘皆ok
        random_online = random.sample(online,k=3)    #抽出在線上的k個人
        for n in range(4):
            group_name = random.sample(random_online,k=1) #每組k個
            await ctx.send(f'{n+1}小隊: '+ str(group_name))
            for i in group_name:
                 random_online.remove(i)




def setup(bot):
    bot.add_cog(Main(bot))