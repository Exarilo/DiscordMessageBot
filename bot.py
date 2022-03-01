#---------------------------------------------------------------------------------------------------------------------    
#----------------------------------------------COMMON-----------------------------------------------------------------    
#---------------------------------------------------------------------------------------------------------------------    
from pickle import TRUE
import discord
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
import discord.ext.commands as commands
from fpdf import FPDF
from dotenv import load_dotenv
from Twitter import *
from Instagram import *



load_dotenv()
client = commands.Bot("!")

DiscordComponents(client)

@client.command()
async def begin(ctx):
    #await ctx.guild.create_category_channel("Reseaux Sociaux")
    channelToCreate=["✅twitter","✅instagram","messenger","facebook","snapchat","tiktok","whatsapp","pas-repondu"]
    
    for i in range(len(channelToCreate)):
        await ctx.guild.create_text_channel(channelToCreate[i],position=i)
    existing_channel = discord.utils.get(ctx.guild.channels).guild.channels
    await createButton(ctx,channelToCreate,True)

@client.command()
async def stop(ctx):
    channelToDelete=["✅twitter","✅instagram","messenger","facebook","snapchat","tiktok","whatsapp","pas-repondu"]

    existing_channel = discord.utils.get(ctx.guild.channels).guild.channels
    for i in range (len(channelToDelete)):
        for j in range (len(existing_channel)):
            if(channelToDelete[i] in existing_channel[j].name):
                await discord.utils.get(ctx.guild.channels, name=channelToDelete[i]).delete()
                break



async def createButton(ctx,channels,isSignIn):
    
    channelToCreate=channels
    existing_channel = discord.utils.get(ctx.guild.channels).guild.channels
    for j in range (len(channelToCreate)):
        for k in range (len(existing_channel)):
            if(channelToCreate[j] in existing_channel[k].name):
                if(isSignIn==True): 
                    await ctx.guild.channels[k].send("Please sign in before using this channel",components = [[Button(label="Sign in", style="1", custom_id="btSignIn"),Button(label="Delete channel", style="4", custom_id="btDeleteChan")]])
                else:
                    if(channelToCreate[j] =="✅instagram"):
                        await ctx.guild.channels[k].send("What do you want to do?",components = [[Button(label="Feed", style="1", custom_id="btFeed"),Button(label="Update channel", style="3", custom_id="btUpdate"), Button(label="Delete Messages", style="4", custom_id="btDelete")]])
                    else:
                        await ctx.guild.channels[k].send("What do you want to do?",components = [[Button(label="Update channel", style="3", custom_id="btUpdate"), Button(label="Delete Messages", style="4", custom_id="btDelete")]])
    while True:
        interaction = await client.wait_for("button_click")




@client.event
async def on_button_click(interaction):
    if interaction.component.label =="Sign in":
        await interaction.channel.purge()  
        if(interaction.channel.name=="✅twitter"):
            await SignInTwitter(ctx=interaction.channel,client=client)
        elif(interaction.channel.name=="✅instagram"):
            await SignInInstagram(ctx=interaction.channel,client=client)
        await createButton(interaction.channel,channels = [interaction.channel.name],isSignIn=False)
    if interaction.component.label =="Feed":
        await interaction.channel.purge()  
        #await feed(ctx=interaction.channel)
        await createButton(interaction.channel,channels = [interaction.channel.name],isSignIn=False)
    elif interaction.component.label =="Update channel":
        await interaction.channel.purge()  
        if interaction.channel.name =="✅twitter":
            await updateTwitter(ctx=interaction.channel)
        elif interaction.channel.name =="✅instagram":
            #await updateInstagram(ctx=interaction.channel)    
            a=1
        #await createButton(interaction.channel,channels = [interaction.channel.name],isSignIn=False)
    elif interaction.component.label =="Delete Messages":
        await interaction.channel.purge()  
        await createButton(interaction.channel,channels = [interaction.channel.name],isSignIn=False)  


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





            
@client.event
async def on_reaction_add(reaction, user):
    if user != client.user:
        if str(reaction.emoji) == "❌":
            await reaction.message.delete()
    


@client.command()
async def send(ctx,*,message):
    if(len(ctx.message.mentions)>0):
        if(ctx.message.mentions[0].name=="MessagesBot"):
            Twitter.api.update_status(in_reply_to_status_id=int(tweetByIDs.get(ctx.message.reference.message_id)[0]), status="@"+tweetByIDs.get(ctx.message.reference.message_id)[1]+" "+message)
            
    else:
        Twitter.api.update_status(status=message,auto_populate_reply_metadata=True)

    #PARAM = {"text": mytext, "reply": {"in_reply_to_tweet_id": id}}

    await ctx.channel.send("Message sended !")









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
def InitServ():
    handler_object = MyHttpRequestHandler
    PORT = 8000
    my_server = socketserver.TCPServer(("", PORT), handler_object)
    my_server.handle_request()

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        query_components = parse_qs(urlparse(self.path).query)
        html = f"<html><head></head><body><h1>Hello !</h1></body></html>"
        self.wfile.write(bytes(html, "utf8"))
        oAuth.OauthVerifier=query_components['oauth_verifier'][0]
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


#app = Flask('app')
#@app.route('/')

#def run():
#    return '<h1>Hello, Server!</h1>'

#app.run(host = '0.0.0.0', port = 8080)

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


