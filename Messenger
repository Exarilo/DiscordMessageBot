from fbchat import Client
from fbchat.models import *
import discord
import discord.ext.commands as commands
import fbchat
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
from messenger_api import Messenger
import fbchat
import re

class Messenger2:
    #accessToken = ""
    #accessTokenExpireIn=""
    #userID=""
    ButtonsSignIn = [Button(label="Sign in", style="1", custom_id="btSignIn"),Button(label="Delete channel", style="4", custom_id="btDeleteChan")]
    ButtonsUpdates=[Button(label="Direct Message", style="3", custom_id="btMessage"),Button(label="Delete Messages", style="4", custom_id="btDelete")]

    async def SignInMessenger(ctx,client):
        fbchat._util.USER_AGENTS    = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"]
        fbchat._state.FB_DTSG_REGEX = re.compile(r'"DTSGInitialData",\[\],{"token":"(.*?)"')
        client=fbchat.Client()
        fbchat.c
        embed=discord.Embed(title="ENTER YOUR USERNAME : ",url="https://replit.com/",description="")
        await ctx.send(embed=embed)
        msg = await client.wait_for('message', check=None, timeout=None)
        await ctx.purge()
        username=msg.content
        embed=discord.Embed(title="ENTER YOUR PASSWORD : ",url="https://replit.com/",description="")
        await ctx.send(embed=embed)
        msg2 = await client.wait_for('message', check=None, timeout=None)
        await ctx.purge()
        password=msg2.content
        msg2 = await ctx.send("Connecting your account ...")
        log = Messenger(username, password)
        
        #userInfo=cl.user_info(cl.user_id)
        #User.pk=userInfo.pk
        #User.username=userInfo.username
        #User.pic=userInfo.profile_pic_url

        embed=discord.Embed(title=User.username,description="succefuly connected !", url="https://www.instagram.com", color=0x1fa335)
        embed.set_image(url=User.pic)
        await msg2.delete()
        await ctx.send(embed=embed)
