import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import time
import json,asyncio,datetime

class Level(Cog_Extension):

    @commands.Cog.listener()
    async def on_message(self,message):

        async def add_experience(users_level_info, user, exp):          
            if (time.time() - users_level_info[str(user.id)]["last_message"] > 1): 
                users_level_info[str(user.id)]["experience"] += exp
                users_level_info[str(user.id)]["last_message"] = time.time()
            else:
                return

        async def level_up(users_level_info, user, channel):
            experience = users_level_info[str(user.id)]["experience"]
            coin = users_level_info[str(user.id)]["coin"]
            lvl_start = users_level_info[str(user.id)]["level"]
            lvl_end = int(experience ** (1/4))

            if lvl_start < lvl_end: #升等時
                await channel.send(f":tada: 恭喜 {user.mention}！你已經將等級升到了 {lvl_end}，並獲得{lvl_end*2}的金幣！!")
                users_level_info[str(user.id)]["level"] = lvl_end
                users_level_info[str(user.id)]["coin"] =  coin+lvl_end*2 #給等級兩倍的金幣

                if lvl_end == 4:
                    guild =self.bot.get_guild(int(jdata['guild']))
                    
                    touristRole = guild.get_role(int(jdata['tourist_role_id']))
                    citizecRrole = guild.get_role(int(jdata["citizec_role_id"]))
                    await user.remove_roles(touristRole)
                    await user.add_roles(citizecRrole)
                    await user.send(f'你獲得了{citizecRrole}身分組')

        with open('setting.json', 'r') as f:
                jdata = json.load(f)

        if (message.author.bot == False) & (message.channel.id != int(jdata['Welcome_channel'])) & (message.channel.id != int(jdata['punch_channel'])):
            with open('users_level.json', 'r') as f:
                users_level_info = json.load(f)

            await add_experience(users_level_info, message.author, 10)
            await level_up(users_level_info, message.author,self.bot.get_channel(int(jdata['level_channel']))) 

            with open('users_level.json', 'w') as f:  
                json.dump(users_level_info, f,indent=4)

        # await self.bot.process_commands(message) #看不出來目前有甚麼特別作用，但會讓commend重複兩次???????????????
       

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
   
        async def time_task(): #bot在特定時間運行
            await self.bot.wait_until_ready() #bot開啟後
            while not self.bot.is_closed(): #當機器人開啟時
                now_time = datetime.datetime.now().strftime('%m%d') #選擇時間要的格式
                with open('setting.json',mode = 'r',encoding='utf8') as jfile:
                    jdata = json.load(jfile)
                
                guild =self.bot.get_guild(int(jdata['guild']))
                citizecRole = guild.get_role(int(jdata['citizec_role_id']))
                localRole = guild.get_role(int(jdata['local_role_id']))
                powerfulRole = guild.get_role(int(jdata['powerful_role_id']))
                role_channel = self.bot.get_channel(int(jdata['role_channel'])) #要傳入的頻道
                
                with open('users_level.json', 'r') as f:
                    users_level_info = json.load(f)
                
                if now_time == jdata["role_change_time"]:   
                    user_id_ex = []
                    for i in users_level_info:
                        temporary_storage = [] #暫存
                        user_id = i
                        user_ex = users_level_info[i]['experience']
                        if user_ex < 256:
                            break
                        temporary_storage.append(user_id)
                        temporary_storage.append(user_ex)
                        user_id_ex.append(temporary_storage) #id和經驗換成list
        
                    sort = sorted(user_id_ex, key = lambda s: s[1],reverse = True)
                    print(sort)
                    for i in range (0,int(len(sort))): #先將3種身分刪除
                        id = int(sort[0:int(len(sort))][i][0])
                        member = guild.get_member(id)
                        print(member.roles)
                        if citizecRole in member.roles:
                            await member.remove_roles(citizecRole)
                        if localRole in member.roles:
                            await member.remove_roles(localRole)
                        if powerfulRole in member.roles:
                            await member.remove_roles(powerfulRole)
                    
   
                    for i in range (int(len(sort)/10)): #前10%為權望人士
                        id = int(sort[0:int(len(sort)/10)][i][0])
                        member = guild.get_member(id)
                        await role_channel.send('下列使用者為權狀領袖')
                        await role_channel.send(f"{member.mention}")
                        await member.add_roles(powerfulRole) 
                    

                    for i in range (int(len(sort)/10),int(len(sort)/4)): #10%~25%為地方領袖
                        id = int(sort[int(len(sort)/10):int(len(sort)/4)][i][0])
                        member = guild.get_member(id)
                        await role_channel.send('下列使用者為地方領袖')
                        await role_channel.send(f"{member.mention}")
                        await member.add_roles(localRole)
                    
                    for i in range (int(len(sort)/4),int(len(sort))): #25%~原本至少擁有市民身分證的人還是市民
                        id = int(sort[int(len(sort)/4):int(len(sort))][i][0])
                        member = guild.get_member(id)
                        await role_channel.send('下列使用者為市民')
                        await role_channel.send(f"{member.mention}")
                        await member.add_roles(citizecRole)
                    

                    if (jdata["role_change_time"][0] == '0') & (jdata["role_change_time"][1] == '9'): #九月的情形
                        jdata["role_change_time"] = str(int(jdata["role_change_time"])+100)
                    elif jdata["role_change_time"][0] == '0': #一月到八月
                        jdata["role_change_time"] = '0' + str(int(jdata["role_change_time"])+100)
                    elif jdata["role_change_time"] == '1201': #十二月轉回一月的情形
                        jdata["role_change_time"] = '0101'
                    else: #十月與十一月之情形
                        jdata["role_change_time"] = str(int(jdata["role_change_time"])+100)                     
                    
                    with open('setting.json',mode = 'w',encoding='utf8') as jfile:
                        json.dump(jdata,jfile,indent=4)
                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(1)
                    pass
        self.bg_task = self.bot.loop.create_task(time_task())



def setup(bot):
    bot.add_cog(Level(bot))