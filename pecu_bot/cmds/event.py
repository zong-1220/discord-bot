from ast import keyword
from email import message
from turtle import update
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('setting.json',mode = 'r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Event(Cog_Extension): 
    @commands.Cog.listener() #成員加入 #正確
    async def on_member_join(self,member):
        # 給Stranger身份
        guild = self.bot.get_guild(member.guild.id)
        strangerRole = guild.get_role(int(jdata['stranger_role_id']))
        await member.add_roles(strangerRole)
        await member.send(f"你現在是此頻道的{strangerRole}！") #私


    @commands.Cog.listener() #成員退出  #沒辦法傳訊息給用戶
    async def on_member_remove(self,member):
        with open('users_level.json', 'r') as f:
                users_level_info = json.load(f)
        if str(member.id) in users_level_info:         
            users_level_info.pop(str(member.id)) #刪除在users_level的資料


    @commands.Cog.listener() #正確
    async def on_message(self, msg):
    # 自我介紹後，移除stranger，新增遊客
        with open('users_level.json', 'r') as f:
            users_level_info = json.load(f)
        with open('setting.json', 'r') as f:
            jdata = json.load(f)

        guild =self.bot.get_guild(int(jdata['guild']))
        strangerRole = guild.get_role(int(jdata['stranger_role_id']))
        touristRole = guild.get_role(int(jdata['tourist_role_id']))
        user = guild.get_member(msg.author.id)
       
        # 在自我介紹頻道發言的情況下，(有關鍵字 & 不在json) 
        if (msg.channel.id==int(jdata['Welcome_channel'])):
            if (str(msg.author.id) not in users_level_info):
                if ("嗨" in msg.content):
                    users_level_info[str(user.id)] = {}
                    users_level_info[str(user.id)]["experience"] = 0
                    users_level_info[str(user.id)]["level"] = 1
                    users_level_info[str(user.id)]["coin"] = 0
                    users_level_info[str(user.id)]["last_message"] = 0
                    users_level_info[str(user.id)]["inRow"] = 0
                    users_level_info[str(user.id)]["lastPunch"] = 0
                    users_level_info[str(user.id)]["lastestPunch"] = 0
                    with open('users_level.json', 'w') as f:  
                        json.dump(users_level_info, f,indent=4)
                    await user.remove_roles(strangerRole)
                    await user.add_roles(touristRole)
                    await user.send(f"恭喜你完成自我介紹，現在你是PecuLab的{touristRole}！")
                else:
                    await msg.channel.purge(limit = 1)
                    await user.send(f"你的自我介紹:\n{msg.content}")
                    await user.send("你的自我介紹好像沒有照格式來喔！再修改一下吧~")
            else:
                return






    # 處裡"指令"發生之錯誤 Error Handler
    # 也可做獨立"指令"的錯誤訊息(EP15 29:00)
    @commands.Cog.listener() 
    async def on_command_error(self,ctx,error):
        if isinstance(error,commands.errors.MissingRequiredArgument):
            await ctx.send('記得輸入參數喔！')
        elif isinstance(error,commands.errors.BadArgument):
            await ctx.send('參數型態錯了啦！')
        elif isinstance(error,commands.errors.CommandNotFound):
            await ctx.send('沒有這個指令喔！')
        else:
            await ctx.send('發生錯誤，再注意一下哪錯了！')
    

def setup(bot):
    bot.add_cog(Event(bot))







