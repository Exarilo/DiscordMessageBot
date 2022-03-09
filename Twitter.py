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

class UserTweets:
    listTweets=[]
    currentTweetIndex=0
class UserMessages:
    listID=[]
    listMessages=[]
    currentMessageIndex=0
    MessageByID = {} 
class Twitter:
    api = ""
    userName=""
    userID=""
    currentTweetId=""
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

    async def getUserMessages(ctx):
        messages=Twitter.api.get_direct_messages()['events']

        if(len(messages)==0):
            await ctx.send("No messages found !")
            return
#-----------------------------------------------------
#-----------------------------------------------------
#1 recipient contient : 
#1 userID --> listMessages
#1 userId --> listMessages

        for i in range(len(messages),0):
            if(messages[i]['message_create']['target']['recipient_id'] in UserMessages.MessageByID):
                UserMessages.MessageByID[messages[i]['message_create']['target']['recipient_id']].insert(len(UserMessages.MessageByID[messages[i]['message_create']['sender_id']]),messages[i]['message_create']['message_data']['text'],messages[1]['message_create']['sender_id'])
            else:
                UserMessages.MessageByID[messages[i]['message_create']['target']['recipient_id']]=[messages[i]['message_create']['message_data']['text'],messages[1]['message_create']['sender_id']]
                UserMessages.listID.append(messages[i]['message_create']['target']['recipient_id'])
#-----------------------------------------------------
#-----------------------------------------------------


        for i in range(len(messages)):
            if(messages[len(messages)-i-1]['message_create']['sender_id'] in UserMessages.MessageByID):
                UserMessages.MessageByID[messages[len(messages)-i-1]['message_create']['sender_id']].insert(len(UserMessages.MessageByID[messages[len(messages)-i-1]['message_create']['sender_id']]),messages[len(messages)-i-1]['message_create']['message_data']['text'])
            else:
                UserMessages.MessageByID[messages[len(messages)-i-1]['message_create']['sender_id']]=[messages[len(messages)-i-1]['message_create']['message_data']['text']]
                UserMessages.listID.append(messages[len(messages)-i-1]['message_create']['sender_id'])
        await Twitter.setMessagesEmbed(ctx)

    async def setMessagesEmbed(ctx):
        user=Twitter.api.show_user(id=UserMessages.listID[UserMessages.currentMessageIndex])    
        
        UserMessages.MessageByID[UserMessages.listID[UserMessages.currentMessageIndex]]
        
        embed=discord.Embed(title="MESSAGES",url="https://twitter.com/home",color=0xbe6e2d)
        embed.set_thumbnail(url=user['profile_image_url'])
        
        for i in range(len(UserMessages.MessageByID[UserMessages.listID[UserMessages.currentMessageIndex]])):
            embed.add_field(name=user['name'], value=UserMessages.MessageByID[UserMessages.listID[UserMessages.currentMessageIndex]][i], inline=False)
        await ctx.send(embed=embed)
        
        
        
        
        

        '''
        
        async def getUserTweets(ctx):
                Tweets=Twitter.api.get_user_timeline()
                if(len(Tweets)==0):
                    await ctx.send("No tweets found")
                    return
                
                UserTweets.listTweets.append(Tweets)
                OriginalTweet=Twitter.api.show_status(id=UserTweets.listTweets[0][UserTweets.currentTweetIndex]['in_reply_to_status_id'])
                
                embed=discord.Embed(title="TWEETS",url="https://twitter.com/home",color=0x9e65d7)
                embed.set_thumbnail(url=OriginalTweet['user']['profile_image_url'])
                embed.add_field(name=OriginalTweet['user']['name'],value=OriginalTweet['text'])
                embed.add_field(name=OriginalTweet['user']['name'],value=OriginalTweet['text'])
                await ctx.send(embed=embed)
                
                Twitter.api.lookup_status(id=1491462040619204617)

                for tweet in Tweets:
                    print(tweet['text'], tweet['created_at'])
                    last_id = tweet['id']

    '''
            

    async def updateTwitter2(ctx):
        #a=Twitter.api.get_list_statuses()
        a=Twitter.api.get_home_timeline()
        b=Twitter.api.get_direct_messages()
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

            if(isOriginalFound==False):
                OriginalTweet = Twitter.api.show_status(id=ReplytweetID)
                OriginalText=OriginalTweet["text"]
                OriginalName=OriginalTweet["user"]["name"]
                OriginalProfilImage=OriginalTweet["user"]["profile_image_url"]
                Twitter.currentTweetId=OriginalTweet['id']
                isOriginalFound=True
            
                embed=discord.Embed(title=OriginalName,url="https://twitter.com/home", description=OriginalText, color=discord.Color.blue())   
                embed.set_thumbnail(url=OriginalProfilImage)
            embed.add_field(name=ReplyName,value=Replytext)
        message = await ctx.send(embed=embed)  
        await message.add_reaction('◀️')
        await message.add_reaction('▶️')   
