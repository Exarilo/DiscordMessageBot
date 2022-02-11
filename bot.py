from pickle import TRUE
from tkinter.ttk import Style
from turtle import position
import discord
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
import discord.ext.commands as commands
import twitter
import json
from io import BytesIO
from fpdf import FPDF
import requests
from PIL import Image
#from discord_ui import Button,ButtonStyle,UI, LinkButton,SelectMenu, SelectOption




# set up the client

client = commands.Bot("!")
DiscordComponents(client)
api = twitter.Api(consumer_key="LqSTKJ8gmIxmiva9CnZz5etpx",
                  consumer_secret="aepOY73TBXCzLCrfHt6n2TiaOGbdkxDa5al40ge2T9bK5ayLiU",
                  access_token_key="1491038401641992196-xrMnwLb6RzsmWsw2r929YOFg59GVM7",
                  access_token_secret="W4hal073NXJWYqPxmYlOBq0ELQ5JIyEAoAwoUz41rcfii")




'''
@client.command()
async def ggg(ctx):
    await ctx.send(
        "Hello, World!",
        components = [
            Button(label = "WOW button!", custom_id = "button1")
        ]
    )
    interaction = await client.wait_for("button_click", check = lambda i: i.custom_id == "button1")
    await interaction.send(content = "Button clicked!")
'''


    

@client.command()
async def begin(ctx):
    #await ctx.guild.create_category_channel("Reseaux Sociaux")
    channelToCreate=["✅twitter","instagram","messenger","facebook","snapchat","tiktok","whatsapp","pas-repondu"]
    for i in range(len(channelToCreate)):
        await ctx.guild.create_text_channel(channelToCreate[i],position=i)
    existing_channel = discord.utils.get(ctx.guild.channels).guild.channels
    
    for j in range (len(channelToCreate)):
        for k in range (len(existing_channel)):
            if(channelToCreate[j] in existing_channel[k].name):
                await ctx.guild.channels[k].send("What do you want to do?",components = [
                    [Button(label="Update channel", style="3", custom_id="button1"), Button(label="Delete Messages", style="4", custom_id="button2")]
                    ])
    while True:
        interaction = await client.wait_for("button_click")

   

@client.event
async def on_button_click(interaction):
    if interaction.component.label =="Update channel":
        if interaction.channel.name =="✅twitter":
            await interaction.channel.last_message.delete()
            await updateTwitter(ctx=interaction.channel)
    if interaction.component.label =="Delete Messages":
        await interaction.channel.purge()    
    



@client.command()
async def stop(ctx):
    channelToDelete=["✅twitter","instagram","messenger","facebook","snapchat","tiktok","whatsapp","pas-repondu"]

    existing_channel = discord.utils.get(ctx.guild.channels).guild.channels
    for i in range (len(channelToDelete)):
        for j in range (len(existing_channel)):
            if(channelToDelete[i] in existing_channel[j].name):
                await discord.utils.get(ctx.guild.channels, name=channelToDelete[i]).delete()
                break










#@client.command()


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
            isOriginalFound=True
            await ctx.send("**--------------------- New Message ---------------------**",embed=embed)
        isOriginalFound=True
        embed=discord.Embed(title=ReplyName,url="https://twitter.com/home", description=Replytext, color=discord.Color.red())   
        embed.set_thumbnail(url=ReplyProfilImage)
        await ctx.send(embed=embed)   



@client.command()
async def send(ctx,*,name):
    api.PostUpdate(status=name)
    await ctx.channel.send("Message sended !")
    
    
@client.command()
async def button(ctx):
    await ctx.send("What do you want to do?",components = [
        [Button(label="Update channel", style="3", custom_id="button1"), Button(label="Delete Messages", style="4", custom_id="button2")]
        ])
    interaction = await client.wait_for("button_click")

    while True:
        if interaction.component.label =="Update channel":
            await interaction.send(content = "Update channel ", ephemeral=False)
            await ctx.message.delete()
            await updateTwitter(ctx=ctx)
        if interaction.component.label =="Delete Messages":
            await interaction.send(content = "Delete Begin!", ephemeral=False)
            await ctx.channel.purge()
        


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
            await ctx.send("urmom")
    

client.run('OTQwNjI3ODE2MjQ3MDk5NDgz.YgKJ6w.YeVxuK-nBBkNfh0fOnjrvyM_Xe4')




'''
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
# set up the client

client = commands.Bot("!")
DiscordComponents(client)
api = twitter.Api(consumer_key="LqSTKJ8gmIxmiva9CnZz5etpx",
                  consumer_secret="aepOY73TBXCzLCrfHt6n2TiaOGbdkxDa5al40ge2T9bK5ayLiU",
                  access_token_key="1491038401641992196-xrMnwLb6RzsmWsw2r929YOFg59GVM7",
                  access_token_secret="W4hal073NXJWYqPxmYlOBq0ELQ5JIyEAoAwoUz41rcfii")

#@client.command()


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
            await ctx.send("**--------------------- New Message ---------------------**",embed=embed)
        isOriginalFound=True
        embed=discord.Embed(title=ReplyName,url="https://twitter.com/home", description=Replytext, color=discord.Color.red())   
        embed.set_thumbnail(url=ReplyProfilImage)
        await ctx.send(embed=embed)   



@client.command()
async def send(ctx,*,name):
    api.PostUpdate(status=name)
    await ctx.channel.send("Message sended !")
    
    
@client.command()
async def button(ctx):
    await ctx.send("What do you want to do?",components = [
        [Button(label="Update channel", style="3", custom_id="button1"), Button(label="Delete Messages", style="4", custom_id="button2")]
        ])
    interaction = await client.wait_for("button_click")

    while True:
        if interaction.component.label =="Update channel":
            await interaction.send(content = "Update channel ", ephemeral=False)
            await ctx.message.delete()
            await update(ctx=ctx)
        if interaction.component.label =="Delete Messages":
            await interaction.send(content = "Delete Begin!", ephemeral=False)
            await ctx.channel.purge()
        


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
            await ctx.send("urmom")
    

client.run('OTQwNjI3ODE2MjQ3MDk5NDgz.YgKJ6w.YeVxuK-nBBkNfh0fOnjrvyM_Xe4')
'''
