import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json
import time
import datetime

with open('setting.json',mode = 'r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class React(Cog_Extension):
    @commands.command()
    async def punch(self, ctx):
        with open('users_level.json', 'r') as f:
            users_level_info = json.load(f)
    
        user = ctx.author
        now = datetime.datetime.now()
        lastestPunch = users_level_info[str(user.id)]["lastestPunch"]

        print("初次打卡",lastestPunch,type(lastestPunch))
        ## 初次打卡
        if lastestPunch == 0:
            users_level_info[str(user.id)]["lastestPunch"] = now.strftime("%Y-%m-%d %H:%M:%S")
            embed=discord.Embed(title="打卡成功 ⏰", description=f"恭喜 {user.mention}完成第一次打卡，獲得經驗值+5🔋", color=0x3098e8)
            embed.add_field(name="本次打卡時間", value=users_level_info[str(user.id)]["lastestPunch"], inline=True)
            await ctx.send(embed=embed)
            users_level_info[str(user.id)]["inRow"] = 1
            users_level_info[str(user.id)]["experience"] += 5
            print("第一次打卡")
    
        else:
            lastPunch = datetime.datetime.strptime(lastestPunch, "%Y-%m-%d %H:%M:%S")
            print("last min", lastPunch.minute)
            print(type(lastPunch.minute))
            print("now", now, "last", lastPunch)
            print('day',lastPunch.day)

            ## 打卡失敗 1.重複打卡
            if now.day == lastPunch.day:
                print("重複打卡")
                embed=discord.Embed(title=f"今日已打卡", description=f"請勿重複打卡！！", color=0xbcbab8)
                embed.add_field(name="打卡記錄", value=users_level_info[str(user.id)]["lastestPunch"], inline=True)
                await ctx.send(embed=embed)

            ## 連續成功打卡 1.一班連續 2.連續十天倍數（給金幣）
            elif now.day == lastPunch.day+1:
                print("一分鐘內")
                users_level_info[str(user.id)]["lastPunch"] = users_level_info[str(user.id)]["lastestPunch"]
                users_level_info[str(user.id)]["lastestPunch"] = now.strftime("%Y-%m-%d %H:%M:%S")

                if users_level_info[str(user.id)]['inRow']%10 == 0:
                    embed=discord.Embed(title=f"你已連續打卡{users_level_info[str(user.id)]['inRow']}天🔥", description=f"恭喜 {user.mention}連續打卡成功，獲得經驗值+5🔋以及額外的🪙+10!", color=0xff7e14)
                    embed.add_field(name="本次打卡時間", value=users_level_info[str(user.id)]["lastestPunch"], inline=True)
                    embed.add_field(name="上次打卡時間", value=users_level_info[str(user.id)]["lastPunch"], inline=True)
                    users_level_info[str(user.id)]["coin"]+=10
                    await ctx.send(embed=embed)
                elif users_level_info[str(user.id)]['inRow']%10 != 0:
                    embed=discord.Embed(title=f"你已連續打卡{users_level_info[str(user.id)]['inRow']}天🔥", description=f"恭喜 {user.mention}連續打卡成功，獲得經驗值+5🔋", color=0x3098e8)
                    embed.add_field(name="本次打卡時間", value=users_level_info[str(user.id)]["lastestPunch"], inline=True)
                    embed.add_field(name="上次打卡時間", value=users_level_info[str(user.id)]["lastPunch"], inline=True)
                    await ctx.send(embed=embed)
                users_level_info[str(user.id)]["experience"] += 5
                users_level_info[str(user.id)]["inRow"] += 1


        ## 打卡成功，無連續
            elif now.day != lastPunch.day+1:
                users_level_info[str(user.id)]["lastPunch"] = users_level_info[str(user.id)]["lastestPunch"]
                users_level_info[str(user.id)]["lastestPunch"] = now.strftime("%Y-%m-%d %H:%M:%S")
                embed=discord.Embed(title="打卡成功 ⏰", description=f"恭喜 {user.mention}打卡成功，獲得經驗值+5🔋", color=0x3098e8)
                embed.add_field(name="本次打卡時間", value=users_level_info[str(user.id)]["lastestPunch"], inline=True)
                embed.add_field(name="上次打卡時間", value=users_level_info[str(user.id)]["lastPunch"], inline=True)
                await ctx.send(embed=embed)
                users_level_info[str(user.id)]["inRow"] = 1
                users_level_info[str(user.id)]["experience"] += 5
                print("新的打卡循環")

        print()
        print("idddddd", str(ctx.author.id))
    

        with open('users_level.json', 'w') as f:  
            json.dump(users_level_info, f,indent=4, default=str)
        with open('users_level.json', 'w') as f:  
            json.dump(users_level_info, f,indent=4)

    @commands.command()
    async def 查看錢包(self, ctx):
        user = ctx.message.author
        with open('users_level.json', 'r') as f:
            users_level_info = json.load(f)
        embed=discord.Embed(title="錢包查詢 🔍", description=f"你錢包目前擁有餘額為：{users_level_info[str(user.id)]['coin']} 🪙", color=0x91bafd)
        await user.send(embed=embed)

def setup(bot):
    bot.add_cog(React(bot))