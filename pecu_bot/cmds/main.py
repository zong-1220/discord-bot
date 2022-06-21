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

    @commands.command()
    async def intro_msg(self, ctx):
        newbieChannel = self.bot.get_channel(952012076027621399)
        embed=discord.Embed(title="新進成員注意", description="請到「自我介紹區」讓其他成員認識你吧！", color=0x3098e8)
        embed.add_field(name="如何成為PecuLab一員？", value="① 進行自我介紹以取得遊客身份 \n ② 取得遊客身份時會同時開啟閒聊大廳以及經驗值累計", inline=False)
        embed.add_field(name="自我介紹的格式", value="請複製虛線以下的問題，並針每一項做回覆即可\n --------------------------------------------------------------------\n ① 請和大家介紹你是誰？\n\n ② 為什麼想加入PecuLab \n\n ③ 你能提供什麼（技術、理念等）\n", inline=True)
        # await ctx.send(embed=embed)
        await newbieChannel.send(embed=embed)

       

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