import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json
import time
import datetime

with open('setting.json',mode = 'r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class roleReaction(Cog_Extension):
    @commands.command()
    async def channelem(self, ctx):
        embed=discord.Embed(title="頻道解鎖", description="歡迎點選下方圖示解鎖有興趣的頻道！\n\n 💻 --- 技術交流\n📊 --- 投資理財交流\n👔 --- 學生創業輔導\n🌱 --- sdg4 優質教育\n📈 --- sdg8 合適的工作及經濟成長\n💰 --- sdg12 責任消費及生產", color=0x00a3d7)
        message = await ctx.send(embed = embed)
        newEmbed = await message.add_reaction("💻") #技術交流
        newEmbed = await message.add_reaction("📊") #投資理財
        newEmbed = await message.add_reaction("👔") #創業輔導
        newEmbed = await message.add_reaction("🌱") #sdg4
        newEmbed = await message.add_reaction("📈") #sdg8
        newEmbed = await message.add_reaction("💰") #sdg12
        message.edit(embed = newEmbed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        if str(data.emoji) == '💻': #技術交流
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(int(jdata['tech']))
            await data.member.add_roles(role)
            await data.member.send("你解鎖了技術交流頻道！")

        elif str(data.emoji) == '📊': #投資理財
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(int(jdata['investment']))
            await data.member.add_roles(role)
            await data.member.send("你解鎖了投資理財交流頻道！")

        elif str(data.emoji) == '👔': #創業輔導
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(int(jdata['business']))
            await data.member.add_roles(role)
            await data.member.send("你解鎖了學生創業輔導頻道！")

        elif str(data.emoji) == '🌱': #stranger
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(int(jdata['sdg4']))
            await data.member.add_roles(role)
            await data.member.send("你解鎖了sdg4頻道！")

        elif str(data.emoji) == '📈': #tourist
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(int(jdata['sdg8']))
            await data.member.add_roles(role)
            await data.member.send("你解鎖了sdg8頻道！")
        
        elif str(data.emoji) == '💰': #programmer
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(int(jdata['sdg12']))
            await data.member.add_roles(role)
            await data.member.send("你解鎖了sdg12頻道！")


    

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, data):

        if str(data.emoji) == '💻': #技術交流
            guild = self.bot.get_guild(data.guild_id)
            user = guild.get_member(data.user_id)
            role = guild.get_role(int(jdata['tech']))
            await user.remove_roles(role)
            await user.send(f"你取消觀看了技術交流頻道")

        elif str(data.emoji) == '📊': #投資理財
            guild = self.bot.get_guild(data.guild_id)
            user = guild.get_member(data.user_id)
            role = guild.get_role(int(jdata['investment']))
            await user.remove_roles(role)
            await user.send(f"你取消觀看了投資理財交流頻道")

        elif str(data.emoji) == '👔': #創業輔導
            guild = self.bot.get_guild(data.guild_id)
            user = guild.get_member(data.user_id)
            role = guild.get_role(int(jdata['business']))
            await user.remove_roles(role)
            await user.send(f"你取消觀看了學生創業輔導頻道")

        elif str(data.emoji) == '🌱': #sdg4
            guild = self.bot.get_guild(data.guild_id)
            user = guild.get_member(data.user_id)
            role = guild.get_role(int(jdata['sdg4']))
            await user.remove_roles(role)
            await user.send(f"你取消觀看了sdg4頻道")

        elif str(data.emoji) == '📈': #sdg8
            guild = self.bot.get_guild(data.guild_id)
            user = guild.get_member(data.user_id)
            role = guild.get_role(int(jdata['sdg8']))
            await user.remove_roles(role)
            await user.send(f"你取消觀看了sdg8頻道")
        
        elif str(data.emoji) == '💰': #sdg12
            guild = self.bot.get_guild(data.guild_id)
            user = guild.get_member(data.user_id)
            role = guild.get_role(int(jdata['sdg12']))
            await user.remove_roles(role)
            await user.send(f"你取消觀看了sdg12頻道")




def setup(bot):
    bot.add_cog(roleReaction(bot))