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


class Instagram:
    accessToken = ""
    accessTokenExpireIn=""
    userID=""
    ButtonsSignIn = [Button(label="Sign in", style="1", custom_id="btSignIn"),Button(label="Delete channel", style="4", custom_id="btDeleteChan")]
    ButtonsUpdates=[Button(label="Feed", style="1", custom_id="btFeed"),Button(label="Update channel", style="3", custom_id="btUpdate"),Button(label="Delete Messages", style="4", custom_id="btDelete")]


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

