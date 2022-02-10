import discord
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
import discord.ext.commands as commands
import twitter
import json
# set up the client

client = commands.Bot("!")
DiscordComponents(client)
api = twitter.Api(consumer_key="LqSTKJ8gmIxmiva9CnZz5etpx",
                  consumer_secret="aepOY73TBXCzLCrfHt6n2TiaOGbdkxDa5al40ge2T9bK5ayLiU",
                  access_token_key="1491038401641992196-xrMnwLb6RzsmWsw2r929YOFg59GVM7",
                  access_token_secret="W4hal073NXJWYqPxmYlOBq0ELQ5JIyEAoAwoUz41rcfii")



#@client.command()
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
