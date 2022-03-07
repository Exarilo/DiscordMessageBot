#---------------------------------------------------------------------------------------------------------------------    
#----------------------------------------------TWITTER----------------------------------------------------------------    
#---------------------------------------------------------------------------------------------------------------------   
import os
from twython import Twython
import discord
import discord.ext.commands as commands
import requests
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select


tweetByIDs = {}  #Key =Discord chat ID #Value = tweetID

class Twitter:
    api = ""
    userName=""
    userID=""
    ButtonsSignIn = [Button(label="Sign in", style="1", custom_id="btSignIn"),Button(label="Delete channel", style="4", custom_id="btDeleteChan")]
    ButtonsUpdates=[Button(label="Update channel", style="3", custom_id="btUpdate"),Button(label="Delete Messages", style="4", custom_id="btDelete")]


    async def SignInTwitter(ctx,client):
        APP_KEY = os.getenv("APP_KEY")
        APP_SECRET = os.getenv("APP_SECRET")
        
        twitter = Twython(APP_KEY, APP_SECRET, oauth_version=1)
        auth = twitter.get_authentication_tokens(force_login=True,callback_url="oob")
        twitter = Twython(APP_KEY, APP_SECRET,auth['oauth_token'], auth['oauth_token_secret'])   
        
        embed=discord.Embed(title="CLICK HERE TO LOGIN", url=auth['auth_url'],description="When you are done please enter the code in chat")
        await ctx.send(embed=embed)
        msg = await client.wait_for('message', check=None, timeout=None)
        await ctx.purge()
        pin=msg.content
        url="https://api.twitter.com/oauth/access_token?oauth_verifier="+str(pin)+"&oauth_token="+str(auth['oauth_token'])
        response = requests.get(url)
        
        Twitter.api=Twython(app_key=APP_KEY,
                        app_secret=APP_SECRET,
                        oauth_token=response.text.split("&")[0].split("=")[1],
                        oauth_token_secret=response.text.split("&")[1].split("=")[1])



        Twitter.userName=response.text.split("&")[3].split("=")[1]
        Twitter.userID=response.text.split("&")[2].split("=")[1]
    async def updateTwitter(ctx):
        Mentions = Twitter.api.get_mentions_timeline()
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
                OriginalTweet = Twitter.api.show_status(id=ReplytweetID)
                OriginalText=OriginalTweet["text"]
                OriginalName=OriginalTweet["user"]["name"]
                OriginalProfilImage=OriginalTweet["user"]["profile_image_url"]
                embed=discord.Embed(title=OriginalName,url="https://twitter.com/home", description=OriginalText, color=discord.Color.blue())   
                embed.set_image(url=OriginalProfilImage)
                message =await ctx.send("**--------------------- New Message ---------------------**",embed=embed)
                tweetByIDs[message.id] =[OriginalTweet['id'],OriginalTweet["user"]["name"]]
                await message.add_reaction('❌')
                isOriginalFound=True
            embed=discord.Embed(title=ReplyName,url="https://twitter.com/home", description=Replytext, color=discord.Color.red())   
            embed.set_thumbnail(url=ReplyProfilImage)
            message = await ctx.send(embed=embed)  
            tweetByIDs[message.id] = [ReplytweetID,Mentions[i]['in_reply_to_screen_name']]
            await message.add_reaction('❌') 

