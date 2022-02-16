import imp
from pickle import TRUE
import discord
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
import discord.ext.commands as commands
import twitter
import json
from io import BytesIO
from fpdf import FPDF
import requests
from PIL import Image
from dotenv import load_dotenv
import os
import numpy as np
from instagrapi import Client

#from flask import Flask, request


#---------------------------------------------------------------------------------------------------------------------    
#-----------------------------------------------VAR-------------------------------------------------------------------    
#--------------------------------------------------------------------------------------------------------------------- 
load_dotenv()
client = commands.Bot("!")
DiscordComponents(client)
api = twitter.Api(consumer_key=os.getenv("twitterconsumer_key"),
                  consumer_secret=os.getenv("twitterconsumer_secret"),
                  access_token_key=os.getenv("twitteraccess_token_key"),
                  access_token_secret=os.getenv("twitteraccess_token_secret"))

#---------------------------------------------------------------------------------------------------------------------    
#----------------------------------------------COMMON-----------------------------------------------------------------    
#---------------------------------------------------------------------------------------------------------------------    

async def createButton(ctx,channels):
    channelToCreate=channels
    existing_channel = discord.utils.get(ctx.guild.channels).guild.channels
    for j in range (len(channelToCreate)):
        for k in range (len(existing_channel)):
            if(channelToCreate[j] in existing_channel[k].name):
                await ctx.guild.channels[k].send("What do you want to do?",components = [
                    [Button(label="Update channel", style="3", custom_id="button1"), Button(label="Delete Messages", style="4", custom_id="button2")]
                    ])
    while True:
        interaction = await client.wait_for("button_click")

@client.command()
async def begin(ctx):
    #await ctx.guild.create_category_channel("Reseaux Sociaux")
    channelToCreate=["✅twitter","instagram","messenger","facebook","snapchat","tiktok","whatsapp","pas-repondu"]
    
    for i in range(len(channelToCreate)):
        await ctx.guild.create_text_channel(channelToCreate[i],position=i)
    existing_channel = discord.utils.get(ctx.guild.channels).guild.channels
    await createButton(ctx,channelToCreate)

@client.command()
async def stop(ctx):
    channelToDelete=["✅twitter","instagram","messenger","facebook","snapchat","tiktok","whatsapp","pas-repondu"]

    existing_channel = discord.utils.get(ctx.guild.channels).guild.channels
    for i in range (len(channelToDelete)):
        for j in range (len(existing_channel)):
            if(channelToDelete[i] in existing_channel[j].name):
                await discord.utils.get(ctx.guild.channels, name=channelToDelete[i]).delete()
                break


@client.event
async def on_button_click(interaction):
    if interaction.component.label =="Update channel":
        if interaction.channel.name =="✅twitter":
            await interaction.channel.last_message.delete()
            await updateTwitter(ctx=interaction.channel)
            await createButton(interaction.channel,channels = [interaction.channel.name])
    if interaction.component.label =="Delete Messages":
        await interaction.channel.purge()  
        await createButton(interaction.channel,channels = [interaction.channel.name])  

@client.command()
async def pdf(ctx):
    messages = await ctx.channel.history(limit=200).flatten()
    text=""
    for i in messages :
        if (len(i.embeds)!=0):
            message=i.embeds[0].description
            name=i.embeds[0].title
            #img = Image.open(BytesIO(requests.get(str(i.embeds[0].thumbnail.url)).content))
            text+= name+"\n"
            text+= message+"\n"
        else:
            if(i.content !="!pdf" and i.content !="Update channel" and i.content != "What do you want to do?" and i.content !=""):
                text+= i.content+"\n"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.multi_cell(0, 10, text,fill=TRUE)
    bstring = pdf.output(dest='S').encode('latin-1')
    await ctx.send(file=discord.File(BytesIO(bstring), filename='pdf.pdf'))



#---------------------------------------------------------------------------------------------------------------------    
#----------------------------------------------TWITTER-----------------------------------------------------------------    
#---------------------------------------------------------------------------------------------------------------------   
tweetByIDs = {}  #Key =Discord chat ID #Value = tweetID


async def updateTwitter(ctx):
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
            message =await ctx.send("**--------------------- New Message ---------------------**",embed=embed)
            tweetByIDs[message.id] =[OriginalTweet['id'],OriginalTweet["user"]["name"]]
            await message.add_reaction('❌')
            isOriginalFound=True
        embed=discord.Embed(title=ReplyName,url="https://twitter.com/home", description=Replytext, color=discord.Color.red())   
        embed.set_thumbnail(url=ReplyProfilImage)
        message = await ctx.send(embed=embed)  
        tweetByIDs[message.id] = [ReplytweetID,Mentions[i]['in_reply_to_screen_name']]
        await message.add_reaction('❌') 

            
@client.event
async def on_reaction_add(reaction, user):
    if user != client.user:
        if str(reaction.emoji) == "❌":
            await reaction.message.delete()
    


@client.command()
async def send(ctx,*,message):
    if(ctx.message.mentions[0].name=="MessagesBot"):
        api.PostUpdate(in_reply_to_status_id=int(tweetByIDs.get(ctx.message.reference.message_id)[0]), status="@"+tweetByIDs.get(ctx.message.reference.message_id)[1]+" "+message)
        
    else:
        api.PostUpdate(status=message,auto_populate_reply_metadata=True)

    #PARAM = {"text": mytext, "reply": {"in_reply_to_tweet_id": id}}

    await ctx.channel.send("Message sended !")


#---------------------------------------------------------------------------------------------------------------------    
#----------------------------------------------INSTAGRAM--------------------------------------------------------------    
#---------------------------------------------------------------------------------------------------------------------        
InstagramInfo = {} 

@client.command()
async def test2(ctx):
    embed1=discord.Embed(
    title="LISTE DES COMMANDES",
        color=discord.Color.blue())
    embed1.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/fr/thumb/2/2a/Penguin_books.svg/1200px-Penguin_books.svg.png")
    embed1.set_image(url="https://snworksceo.imgix.net/dtc/10ec0a64-8f9d-46d9-acee-5ef9094d229d.sized-1000x1000.jpg?w=1000")
    embed1.add_field(name="`!categorie <nom>`", value="Crée une categorie avec le nom spécifié dans <nom>)", inline=False)    

    embed=discord.Embed(
    title="LISTE DES COMMANDES",
        color=discord.Color.blue())
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/fr/thumb/2/2a/Penguin_books.svg/1200px-Penguin_books.svg.png")
    embed.set_image(url="https://snworksceo.imgix.net/dtc/10ec0a64-8f9d-46d9-acee-5ef9094d229d.sized-1000x1000.jpg?w=1000")
    embed.add_field(name="`!categorie <nom>`", value="Crée une categorie avec le nom spécifié dans <nom>)", inline=False)        
    
    
    url="https://discord.com/api/webhooks/943519534961287178/lMjcnpW3JGzCG9Zop6RFo4z6Z4MYnWVx5_pIyTysWD878i3dL6KvdHkTjZzBIdJqsdR7"

    await ctx.message.create_webhook(name="mywebhook")
    a=1
    #https://discord.com/api/webhooks/943519534961287178/lMjcnpW3JGzCG9Zop6RFo4z6Z4MYnWVx5_pIyTysWD878i3dL6KvdHkTjZzBIdJqsdR7

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


cl = Client()
cl.login("romain.madery92@gmail.com", "dbbe89275c")
@client.command()
async def test(ctx):

    user_id = cl.user_id_from_username("_cryde")
    medias = cl.user_medias(user_id, 20)
    if(len(medias)<=0):
        await ctx.channel.send("No images found")
        return


    #Photo - When media_type=1
    #Video - When media_type=2 and product_type=feed
    #IGTV - When media_type=2 and product_type=igtv
    #Reel - When media_type=2 and product_type=clips
    #Album - When media_type=8

    listPhoto=[]
    for i in range (len(medias)):
        if(medias[i].media_type==1):
            listPhoto.append(medias[i].thumbnail_url)

    for j in range (len(listPhoto)-1):
        imageToSend = Image.open(BytesIO(requests.get(listPhoto[j]).content))
        imagToConcat = Image.open(BytesIO(requests.get(listPhoto[j+1]).content))
        imageToSend=get_concat_h(imageToSend, imagToConcat)



    with BytesIO() as image_binary:
                    imageToSend.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
    a=1
    '''
    api_url = "https://www.instagram.com/exarilosuperbot/channel/?__a=1"
    response = requests.get(api_url)
    response=response.json()
    InstagramInfo["username"] =response['graphql']['user']['full_name']
    InstagramInfo["id"] =response['graphql']['user']['id']
    InstagramInfo["userPicture"] =response['graphql']['user']['profile_pic_url_hd']
    InstagramInfo["userPageId"] =response['logging_page_id']
    node1=response['graphql']['user']['edge_owner_to_timeline_media']['edges']
    listImg=[]
    listMessages=[]
    for i in range(len(node1)) :
        listImg.append(response['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['display_url'])
        node2=response['graphql']['user']['edge_owner_to_timeline_media']['edges'][0]['node']['edge_media_to_caption']['edges']
        for j in range(len(node2)) :
            listMessages.append(response['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['edge_media_to_caption']['edges'][j]['node']['text'])
    InstagramInfo["userPostsImg"] =listImg
    InstagramInfo["userPostsMessages"] =listMessages
    a=1
    #await get_medias("romain_madery")
    '''




#exarilosuperbot=user_id = cl.user_id_from_username(username)
#https://www.instagram.com/exarilosuperbot/?__a=1
#jsonDeseralize
'''
def get_medias(hashtags,
               ht_type='top',
               amount=27,
               ):
    ht_medias = []
    for hashtag in hashtags:
        if ht_type == 'top':
            ht_medias.extend(
                cl.hashtag_medias_top(
                    name=hashtag,
                    amount=amount if amount <= 9 else 9
                )
            )
        elif ht_type == 'recent':
            ht_medias.extend(
                cl.hashtag_medias_recent(
                    name=hashtag,
                    amount=amount
                )
            )
    return list(dict([(media.pk, media) for media in ht_medias]).values())

def getMedias(username: str, amount: int = 5) -> dict:
    amount = int(amount)
    user_id = cl.user_id_from_username(username)
    medias = cl.user_medias(user_id)
    result = {}
    i = 0
    for m in medias:
        if i >= amount:
            break
        paths = []
        if m.media_type == 1:
            # Photo
            paths.append(cl.photo_download(m.pk))
        elif m.media_type == 2 and m.product_type == 'feed':
            # Video
            paths.append(cl.video_download(m.pk))
        elif m.media_type == 2 and m.product_type == 'igtv':
            # IGTV
            paths.append(cl.video_download(m.pk))
        elif m.media_type == 2 and m.product_type == 'clips':
            # Reels
            paths.append(cl.video_download(m.pk))
        elif m.media_type == 8:
            # Album
            for path in cl.album_download(m.pk):
                paths.append(path)
        result[m.pk] = paths
        print(f'http://instagram.com/p/{m.code}/', paths)
        i += 1
    return 


'''



'''
user_id = cl.user_id_from_username("romain_madery")
medias = cl.user_medias(user_id, 20)
media = cl.photo_upload(
    "img.jpg",
    "Test caption for photo with #hashtags and mention users such @adw0rd",
    extra_data={
        "custom_accessibility_caption": "alt text example",
        "like_and_view_counts_disabled": 1,
        "disable_comments": 1,
    }
)


'''










@client.event
async def on_ready():
    print('Ready!')



@client.command()
async def select(ctx):
    await ctx.send("Select", components = [
        Select(
            placeholder = "Select something!",
            options = [
                SelectOption(label="A", value="A"),
                SelectOption(label="B", value="B")
            ]
        )
    ])

    while True:
        try:
            select_interaction = await client.wait_for("select_option")
            await select_interaction.send(content = f"{select_interaction.values[0]} selected!", ephemeral = False)
        except:
            await ctx.send("test")
    

client.run(os.getenv("token"))


