import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json, asyncio, datetime 


# 管理員在指定頻道發訊息後，可以讓Discord Bot代為轉發
# 如何將訊息格式改為embed
# 可以設定時間，時間到了之後自動發出
class Course(Cog_Extension):
    def __init__(self,*args,**kwargs):
      super().__init__(*args,**kwargs)

      self.counter = 0
        
      async def time_task(): #bot在特定時間運行
        await self.bot.wait_until_ready() #bot開啟後
        self.channel = self.bot.get_channel(984576948254687232)
       
        while not self.bot.is_closed():
          
          now_time = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M') #選擇時間要的格式 %Y/%m/%d 
          with open('announce.json',mode = 'r',encoding='utf8') as jfile:
            jdata = json.load(jfile)
         

          class_time = jdata["class"][0]["time"]
          # announce_msg = jdata["announce"][0]["content"]
          # class_msg = jdata["class"][0]["content"]

          if now_time == class_time : #and self.counter==0
            channel = self.bot.get_channel(984576948254687232)

            content_list = []
            fullContent = jdata["class"][0]["content"]
            content = fullContent.split("⍢")

            for i in range(len(content)):
              content_list.append(content[i].split("▻")[1])
            Name = content_list[0]
            Date = content_list[1]
            Location = content_list[2]
            Description = content_list[3]
            publishDate = content_list[4]
              
            embed=discord.Embed(title=f"{Name}", color=0xa8c6fe)
            embed.set_author(name="Pecu", url="https://pecu.github.io/peculab/", icon_url="https://pecu.github.io/peculab/assets/peculabimgs/pecu.jpg")
            embed.set_thumbnail(url="https://pecu.github.io/peculab/assets/peculabimgs/peculab.jpg")
            embed.add_field(name="日期", value=f"{Date}", inline=False)
            embed.add_field(name="地點", value=f"{Location}", inline=False)
            embed.add_field(name="主題介紹", value=f"{Description}")
            embed.set_footer(text=f"發佈時間：{publishDate}")
            await channel.send(embed=embed)
              # await self.channel.send(announce_msg)
            jdata["class"].pop(0)
            with open('announce.json',mode = 'w',encoding='utf8') as jfile:
              json.dump(jdata,jfile,indent=2)
            await asyncio.sleep(1)
          else:
            await asyncio.sleep(1)
            pass


            # if now_time == class_time and self.counter==0:
            #   await self.channel.send(class_msg)
            #   jdata["class"].pop(0)
            #   # self.counter = 1 
            #   await asyncio.sleep(1)
            # else:
            #   await asyncio.sleep(1)
            #   pass

        
      self.bg_task = self.bot.loop.create_task(time_task())


    @commands.command()
    async def ch(self,ctx):

      channel = self.bot.get_channel(984576948254687232)
      await ctx.send("請複製以下格式並在冒號後填入對應內容 \n-------虛線下開始複製-------\n「課程＆公告」\n1. 活動名稱▻⍢\n2. 活動時間▻⍢\n3. 地點▻⍢\n4. 活動介紹▻⍢\n5. 發佈時間▻")

      
      

    @commands.Cog.listener()
    async def on_message(self, msg): ## 記錄課程用
      if "「課程」" in msg.content:
        print(msg.content)
        time = msg.content.split("▻")[-1]

        newData = {"time" : time,"content" : msg.content}
        print(newData)
        
        with open('announce.json', 'r') as f:
          jdata = json.load(f)
        jdata['class'].append(newData)
        jdata["class"].sort(key = lambda k: k.get('time')) #依照時間早到晚排序
        with open('announce.json',mode = 'w',encoding='utf8') as jfile:
          json.dump(jdata,jfile,indent=2)
          
      elif "「公告」" in msg.content:
        print(msg.content)
        time = msg.content.split("▻")[-1]
        newData = {"time" : time,"content" : msg}
        with open('announce.json', 'r') as f:
          jdata = json.load(f)
        jdata['announce'].append(newData)
        jdata["announce"].sort(key = lambda k: k.get('time')) #依照時間早到晚排序
        with open('announce.json',mode = 'w',encoding='utf8') as jfile:
          json.dump(jdata,jfile,indent=2)


    @commands.command()
    async def set_content(self,ctx, category, time, *, msg):

      ## 1. 活動名稱 2. 活動日期 3. 時間 4. 地點 5. 活動介紹 6. 發佈時間
      authorName = ""
      authorProflie = ""
      authorImage = ""
      Name = ""
      Date = ""
      Time = ""
      Location = ""
      Description = ""
      publishDate = ""
      embed=discord.Embed(title=f"{Name}", color=0xa8c6fe)
      embed.set_author(name=f"{authorName}", url=f"{authorProflie}", icon_url=f"{authorImage}")
      embed.add_field(name="日期", value=f"{Date}", inline=True)
      embed.add_field(name="時間", value=f"{Time}", inline=True)
      embed.add_field(name="地點", value=f"{Location}")
      embed.add_field(name="主題介紹", value=f"{Description}")
      embed.set_footer(text=f"發佈時間：{publishDate}")



      newData = {"time" : time,"content" : msg}

      with open('announce.json', 'r') as f:
        jdata = json.load(f)
      if category == "公告":
        jdata['announce'].append(newData)
      elif category == "課程":
        jdata['class'].append(newData)
      jdata["class"].sort(key = lambda k: k.get('time')) #依照時間早到晚排序
      with open('announce.json',mode = 'w',encoding='utf8') as jfile:
        json.dump(jdata,jfile,indent=2)
      
      # if category == "announce":
      #   jdata['announce'] = {
      #     "time" : time,
      #     "content" : msg
      #   }
      # elif category == "class":
      #   jdata['class'] = {
      #     "time" : time,
      #     "contnet" : msg
      #   }
      print("bb")
      msg_channel = ctx.channel
      target_channel = self.bot.get_channel(984577205944328243)
      print(msg_channel,target_channel)
      if (msg_channel == target_channel):
        print("cc")
        await ctx.send(msg)


    @commands.command()
    async def set_anc_time(self,ctx,time):
        self.counter = 0
        with open('setting.json',mode = 'r',encoding='utf8') as jfile:
            jdata = json.load(jfile)
        jdata['time'] = time
        with open('setting.json',mode = 'w',encoding='utf8') as jfile:
            json.dump(jdata,jfile,indent=4)
    
    
    @commands.command()
    async def set_channeld(self,ctx,channel:int):
        self.channel = self.bot.get_channel(channel)
        await ctx.send(f'將訊息傳送到別的頻道(ID):{self.channel.mention}')

def setup(bot):
  bot.add_cog(Course(bot))