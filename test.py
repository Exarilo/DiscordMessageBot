from distutils import command
import discord
from pip._vendor import requests
from discord.ext import commands
import os, time
from datetime import datetime
import twitter
#import facebook
#import fbchat
import getpass
#from fbchat import Client
#from fbchat.models import *
import json
#client = Client("koalasournois2@gmail.com", "dbbe89275c")
#session = fbchat.Client("romain.madery92@gmail.com", "dbbe89275c")
#user = fbchat.User(session=session, id=session.user_id)
#user.send_text("Test message!")





#client.send(Message(text="Hi me!"), thread_id=client.uid, thread_type=ThreadType.USER)

api = twitter.Api(consumer_key="LqSTKJ8gmIxmiva9CnZz5etpx",
                  consumer_secret="aepOY73TBXCzLCrfHt6n2TiaOGbdkxDa5al40ge2T9bK5ayLiU",
                  access_token_key="1491038401641992196-xrMnwLb6RzsmWsw2r929YOFg59GVM7",
                  access_token_secret="W4hal073NXJWYqPxmYlOBq0ELQ5JIyEAoAwoUz41rcfii")


#46679095552a69b900d6809b5685fd93
#import genshinstats as gs

client = discord.Client()
token='OTQwNjI3ODE2MjQ3MDk5NDgz.YgKJ6w.YeVxuK-nBBkNfh0fOnjrvyM_Xe4'



bot = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@bot.command(name="update")
async def update(ctx):
    Mentions = api.GetMentions(return_json=True) 
    isOriginalFound=False
    ReplytweetID=0
    for i in range(len(Mentions)) :
        Replytext= Mentions[i]["text"].partition(' ')[2] 
        if(Mentions[i]["in_reply_to_status_id"]!=ReplytweetID):
            ReplytweetID=Mentions[i]["in_reply_to_status_id"]
            isOriginalFound=False
        else:
            isOriginalFound=True
        ReplyName=Mentions[i]["user"]["name"]
        ReplyProfilImage=Mentions[i]["user"]["profile_image_url"]

        if(isOriginalFound==False):
            OriginalTweet = json.loads(str(api.GetStatus(status_id=ReplytweetID))) 
            OriginalText=OriginalTweet["text"]
            OriginalName=OriginalTweet["user"]["name"]
            OriginalProfilImage=OriginalTweet["user"]["profile_image_url"]
            
            embed=discord.Embed(title=OriginalName,url="https://twitter.com/home", description=OriginalText, color=discord.Color.blue())   
            embed.set_image(url=OriginalProfilImage)
            isOriginalFound=True
            await ctx.send("-----------------------",embed=embed)
        isOriginalFound=True
        embed=discord.Embed(title=ReplyName,url="https://twitter.com/home", description=Replytext, color=discord.Color.red())   
        embed.set_thumbnail(url=ReplyProfilImage)
        await ctx.send(embed=embed)   


         



@bot.command(name="send")
async def send(ctx,*,name):
    api.PostUpdate(status=name)
    await ctx.channel.send("Message sended !")

'''
@bot.command(name="get")
async def get(ctx,*,name):
    api.GetDirectMessages(status=name)
'''


@bot.command(name="supp")
async def delete(ctx, number: int):
    messages = await ctx.channel.history(limit=number + 1).flatten()
    
    for each_message in messages:
        await each_message.delete()


@bot.command(name="categorie")
async def ping(ctx,*,name):
    await ctx.guild.create_category_channel(name, overwrites=None, reason=None, position=None)


   
@bot.command(name="channel")
async def channel(ctx, *,name):
    channel = await ctx.guild.create_text_channel(name+"\n ")
        
   
@bot.command(name="voice")
async def voice(ctx, *,name):
    channel = await ctx.guild.create_voice_channel(name)

    
@bot.command(name='delchannel', help='delete a channel with the specified name')
async def delete_channel(ctx, channel_name):
   existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
   if existing_channel is not None:
      await existing_channel.delete()
   else:
      await ctx.send(f'No channel named, "{channel_name}", was found')


    


@bot.command(name="calc")
async def calc(ctx, operation:str):
  await ctx.send(eval(operation))




bot.run(token)