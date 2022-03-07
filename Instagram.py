#---------------------------------------------------------------------------------------------------------------------    
#----------------------------------------------INSTAGRAM--------------------------------------------------------------    
#---------------------------------------------------------------------------------------------------------------------        
import discord
import discord.ext.commands as commands
import json
from io import BytesIO
import requests
from PIL import Image
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
from instagrapi import Client
import urllib.request
from moviepy.editor import * #pip install MoviePy
#from instagram.client import InstagramAPI
cl = Client()

class Feed:
    listPhoto=[]
    listTxtPhoto=[]
    listVideo=[]
    listTxtVideo=[]
    currentIndex=0
    embed=""
    messageEmbed=""
class User:
    pk=[]
    username = []
    pic = []
    feed=""
class Instagram:
    accessToken = ""
    accessTokenExpireIn=""
    userID=""
    ButtonsSignIn = [Button(label="Sign in", style="1", custom_id="btSignIn"),Button(label="Delete channel", style="4", custom_id="btDeleteChan")]
    ButtonsUpdates=[Button(label="Feed", style="1", custom_id="btFeed"),Button(label="Direct Message", style="3", custom_id="btUpdate"),Button(label="Delete Messages", style="4", custom_id="btDelete")]


    async def SignInInstagram(ctx,client):
        embed=discord.Embed(title="ENTER YOUR USERNAME : ",url="https://www.instagram.com",description="")
        await ctx.send(embed=embed)
        msg = await client.wait_for('message', check=None, timeout=None)
        await ctx.purge()
        username=msg.content
        embed=discord.Embed(title="ENTER YOUR PASSWORD : ",url="https://www.instagram.com",description="")
        await ctx.send(embed=embed)
        msg = await client.wait_for('message', check=None, timeout=None)
        await ctx.purge()
        password=msg.content
        msg = await ctx.send("Connecting your account ...")
        cl.login(username, password)
        userInfo=cl.user_info(cl.user_id)
        User.pk=userInfo.pk
        User.username=userInfo.username
        User.pic=userInfo.profile_pic_url

        embed=discord.Embed(title=User.username,description="succefuly connected !", url="https://www.instagram.com", color=0x1fa335)
        embed.set_image(url=User.pic)
        await msg.delete()
        await ctx.send(embed=embed)


    def fillMediaClass():
        #TypeImg
        medias=cl.user_medias(User.pk,amount=10)
        for i in range (len(medias)):
            if(medias[i].thumbnail_url in Feed.listPhoto):
                continue        
            if(medias[i].media_type==1):
                Feed.listPhoto.append(medias[i].thumbnail_url)
                Feed.listTxtPhoto.append(medias[i].caption_text)
            if(medias[i].media_type==2):
                Feed.listPhoto.append(medias[i].thumbnail_url)
                Feed.listTxtPhoto.append(medias[i].video_url)
            if(medias[i].media_type==8):
                Feed.listPhoto.append(medias[i].resources[0].thumbnail_url)
                Feed.listTxtPhoto.append(medias[i].caption_text)
                '''
                imagConcat = Image.open(BytesIO(requests.get(medias[i].resources[0].thumbnail_url).content))
                for j in range(len(medias[i].resources)):
                    imagToConcat = Image.open(BytesIO(requests.get(medias[0].resources[j].thumbnail_url).content))
                    imagConcat=Instagram.get_concat_v(imagConcat, imagToConcat)   

                Feed.listPhoto.append(imagConcat)
                Feed.listTxtPhoto.append(medias[i].caption_text)
                '''

    def setFeedEmbed():
        embed=discord.Embed(title="FEED INSTAGRAM",url="https://www.instagram.com",color=0xbe6e2d)
        embed.set_author(name=User.username,url=User.pic)
        embed.set_image(url=Feed.listPhoto[Feed.currentIndex])
        if(Feed.listTxtPhoto[Feed.currentIndex][0:4]=="http"):
            embed.add_field(name="-",value="[--> VIDEO LINK <--]("+Feed.listTxtPhoto[Feed.currentIndex]+")",inline=False)
        elif(Feed.listTxtPhoto[Feed.currentIndex]!=""):
            embed.set_footer(text=Feed.listTxtPhoto[Feed.currentIndex])

        Feed.embed=embed


   

    async def getFeedInstagram(ctx):
        Instagram.fillMediaClass()
        Instagram.setFeedEmbed()
        message = await ctx.send(embed=Feed.embed)
        Feed.messageEmbed=message
        await message.add_reaction('◀️')
        await message.add_reaction('▶️')    


    async def getUserMessages(ctx):
        thread=cl.direct_threads(1)[0]
        messages=thread.messages
        embed=discord.Embed(title="MESSAGES", url="https://www.instagram.com",color=0x9e65d7)
        embed.set_thumbnail(url=thread.inviter.profile_pic_url)
        
        for i in range(len(messages)):
            user=cl.user_info(messages[i].user_id)
            embed.add_field(name=user.username, value=messages[i].text, inline=False)
        await ctx.send(embed=embed)

    def get_concat_v(im1, im2):
        dst = Image.new('RGB', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst    
'''

async def getFeedInstagram(ctx):
    User.feed=cl.user_medias(User.pk,amount=10)
    medias=User.feed
    listPhoto=[]
    listPhotoHorizontal=[]
 
    for i in range (len(medias)):
        if(medias[i].media_type==1):
            listPhoto.append(medias[i].thumbnail_url)
    imageToSend=""
    cpt=0
    for j in range (len(listPhoto)-1):
        if(imageToSend==""):
            imagToConcat1 = Image.open(BytesIO(requests.get(listPhoto[j]).content))
            imagToConcat2 = Image.open(BytesIO(requests.get(listPhoto[j+1]).content))
            imageToSend=get_concat_h(imagToConcat1, imagToConcat2)
            cpt+=1
        else:
            imageToSend=get_concat_h(imageToSend, Image.open(BytesIO(requests.get(listPhoto[j+1]).content)))
            cpt+=1
            if(cpt==3):
                listPhotoHorizontal.append(imageToSend)
                imageToSend=""
                cpt=0
                j+=1

    for i in range (len(listPhotoHorizontal)):
        if(i==0):
            imageToSend=listPhotoHorizontal[i]
        else:
            imageToSend=get_concat_v(imageToSend, listPhotoHorizontal[i])
                    
        

    with BytesIO() as image_binary:
                    imageToSend.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst    




async def SignInInstagram(ctx,client):
    embed=discord.Embed(title="CLICK HERE TO LOGIN", url="https://www.instagram.com/oauth/authorize?client_id=448189873753541&redirect_uri=https://zouple.maderyromain.repl.co/&response_type=code&scope=user_profile,user_media",description="When you are done please enter the code in chat")
    await ctx.send(embed=embed)
    msg = await client.wait_for('message', check=None, timeout=None)
    await ctx.purge()
    code=msg.content
    
    url = "https://api.instagram.com/oauth/access_token"
    payload="client_id=448189873753541&redirect_uri=https%3A%2F%2Fzouple.maderyromain.repl.co/&client_secret=0149bba19845b9bcec89ac6de267d554&code="+code+"&grant_type=authorization_code"
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    Instagram.userID=json.loads(response.text)["user_id"]
    url = "https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=0149bba19845b9bcec89ac6de267d554&access_token="+json.loads(response.text)["access_token"]
    response = requests.request("GET", url)


    Instagram.accessToken=json.loads(response.text)["access_token"]
    Instagram.accessTokenExpireIn =json.loads(response.text)["expires_in"]

    
async def getFeedInstagram(ctx):
    url = "https://graph.instagram.com/me/media?fields=id,caption,media_url,media_type&access_token="+Instagram.accessToken

    response = requests.request("GET", url)
    medias=json.loads(response.text)["data"]
    listPhoto=[]
    listPhotoHorizontal=[]
        
    for i in range (len(medias)):
        if(medias[i]["media_type"]=="IMAGE"):
            listPhoto.append(medias[i]["media_url"])
    imageToSend=""
    cpt=0
    for j in range (len(listPhoto)-1):
        if(imageToSend==""):
            imagToConcat1 = Image.open(BytesIO(requests.get(listPhoto[j]).content))
            imagToConcat2 = Image.open(BytesIO(requests.get(listPhoto[j+1]).content))
            imageToSend=get_concat_h(imagToConcat1, imagToConcat2)
            cpt+=1
        else:
            imageToSend=get_concat_h(imageToSend, Image.open(BytesIO(requests.get(listPhoto[j+1]).content)))
            cpt+=1
            if(cpt==3):
                listPhotoHorizontal.append(imageToSend)
                imageToSend=""
                cpt=0
                j+=1

    for i in range (len(listPhotoHorizontal)):
        if(i==0):
            imageToSend=listPhotoHorizontal[i]
        else:
            imageToSend=get_concat_v(imageToSend, listPhotoHorizontal[i])
                    
        

    with BytesIO() as image_binary:
                    imageToSend.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))



'''
