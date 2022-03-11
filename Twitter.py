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
    listSender=[]
    listTxt=[]
    listRecipient=[]
    listUserID=[]
    currentMessageIndex=0
    embed=""
    messageEmbed=""

class Twitter:
    api = ""
    userName=""
    userID=""
    currentTweetId=""
    ButtonsSignIn = [Button(label="Sign in", style="1", custom_id="btSignIn"),Button(label="Delete channel", style="4", custom_id="btDeleteChan")]
    ButtonsUpdates=[Button(label="Direct Message", style="3", custom_id="btMessage"),Button(label="Delete Messages", style="4", custom_id="btDelete"),Button(label="Mentions", style="1", custom_id="btMentions")]
    

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
        user=Twitter.api.show_user(id=Twitter.userID)
        embed=discord.Embed(title=Twitter.userName,description="succefuly connected !", url="https://twitter.com/home", color=0x1fa335)
        embed.set_image(url=user['profile_image_url'])
        await ctx.send(embed=embed)



    async def FillMessagesClass(ctx):
        messages=Twitter.api.get_direct_messages()['events']

        if(len(messages)==0):
            await ctx.send("No messages found !")
            return

        for i in range(len(messages)-1,-1,-1):
            recipientID=messages[i]['message_create']['target']['recipient_id']
            senderID=messages[i]['message_create']['sender_id']
            txt=messages[i]['message_create']['message_data']['text']
            timestamp=messages[i]['created_timestamp']
            
            if(recipientID not in UserMessages.listUserID and Twitter.userID!=recipientID):
                UserMessages.listUserID.append(recipientID)
            if(senderID not in UserMessages.listUserID and Twitter.userID!=senderID):
                UserMessages.listUserID.append(recipientID)

            UserMessages.listRecipient.append(recipientID)
            UserMessages.listSender.append(senderID)
            UserMessages.listTxt.append(txt)


    async def getUserMessages(ctx):
        await Twitter.FillMessagesClass(ctx)
        await Twitter.setMessagesEmbed()
        message = await ctx.send(embed=UserMessages.embed)
        UserMessages.messageEmbed=message
        await UserMessages.messageEmbed.add_reaction('◀️')
        await UserMessages.messageEmbed.add_reaction('▶️')   


    async def setMessagesEmbed():
        user=Twitter.api.show_user(id=UserMessages.listUserID[UserMessages.currentMessageIndex])    
     
        embed=discord.Embed(title="MESSAGES",url="https://twitter.com/home",color=0xbe6e2d)
        embed.set_thumbnail(url=user['profile_image_url'])
        
        for i in range(len(UserMessages.listRecipient)):
            if(UserMessages.listSender[i]==str(user['id'])):
                embed.add_field(name=user['name'], value=UserMessages.listTxt[i], inline=False)
            elif(UserMessages.listSender[i]==Twitter.userID and UserMessages.listRecipient[i]==str(user['id'])):
                embed.add_field(name=Twitter.userName, value=UserMessages.listTxt[i], inline=False)
        UserMessages.embed=embed
        
    async def getMentions(ctx):
        #a=Twitter.api.get_list_statuses()
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
            
                embed=discord.Embed(title="TWEET MENTION",url="https://twitter.com/home", description="", color=discord.Color.blue())   
                embed.add_field(name=OriginalName,value=OriginalText, inline=False)
                embed.set_thumbnail(url=OriginalProfilImage)
            embed.add_field(name=ReplyName,value=Replytext, inline=False)
        message = await ctx.send(embed=embed)  
        await message.add_reaction('◀️')
        await message.add_reaction('▶️')   
        
        
    def setJsonMessage(recipientID,message):
        event = {
            "event": {
                "type": "message_create",
                "message_create": {
                    "target": {
                        "recipient_id": recipientID
                    },
                "message_data": {
                    "text": message
                }
                }
            }
        }
        return event
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
            

