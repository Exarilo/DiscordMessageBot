#---------------------------------------------------------------------------------------------------------------------    
#----------------------------------------------COMMON-----------------------------------------------------------------    
#---------------------------------------------------------------------------------------------------------------------    
from pickle import TRUE
import discord
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select,ButtonStyle
import discord.ext.commands as commands
from fpdf import FPDF
from dotenv import load_dotenv
from Messenger import Messenger, Messenger2
from Twitter import *
from Instagram import *
from Tools import *
import urllib.request as urllib2
import base64
import googleapiclient.discovery #pip install google-api-python-client
import fbchat
import re
import facebook
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument('--log-level=1')
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
driver.get("https://www.facebook.com/") 
email = driver.find_element(By.ID,"email")
email.send_keys("exarildzobot@gmail.com") 
password = driver.find_element(By.ID,"pass")
password.send_keys("acefgdbbe89275c") 
password.send_keys(Keys.RETURN) 
messengerButton=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[2]/div[4]/div[1]/div[2]/span/span/div").click()
a=1



#https://medium.com/mcd-unison/youtube-data-api-v3-in-python-tutorial-with-examples-e829a25d2ebd
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = 'AIzaSyC3buH4EgaLrNj4tD-DyJwBG4kgy-0WklU'

listChannels=["twitter","instagram","messenger","facebook","snapchat","tiktok","whatsapp","pas-repondu"]
load_dotenv()
client = commands.Bot("!")
DiscordComponents(client)


@client.command()
async def test(ctx):
    graph = facebook.GraphAPI(access_token="EAAQM7sdajSkBAC9EHM2w0LNVIchqNMYKDDeBpCldugY1bvRTNaND4wietuZC0Rpqlncc3woaJBr3OJTZCrkBkgIMlLAnKZCJ4zQKPD7pkt6unOu4oa7ZBCPnzSlrSLsr5DfpWy1EKykujBtpwldZCxiCetFIMHUlLJPi1Jm4QZAGHhnZC2zGXbFhZBzrdoMIxbovFzF8ljQxZBwZDZD", version="2.12")
    graph.get_auth_url(1140119593192745,"https://zouple.maderyromain.repl.co",["manage_pages","publish_pages"])
    fbchat._util.USER_AGENTS    = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"]
    fbchat._state.FB_DTSG_REGEX = re.compile(r'"DTSGInitialData",\[\],{"token":"(.*?)"')
    client=fbchat.Client()
    Client()
    fbchat.Client("exasfrilobot@gmail.com","acefgdbbe89275c")

    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)
# 'request' variable is the only thing you must change
# depending on the resource and method you need to use
# in your query
    youtube.search().list(
            part="id,snippet",
            type='video',
            q="Spider-Man",
            videoDuration='short',
            videoDefinition='high',
            maxResults=1
    )
    # Query execution
    #response = request.execute()      
    a=1

@client.command()
async def video(ctx):
        
    ButtonsUpdates=[Button(label="Feed", style="1", custom_id="btFeed"),Button(label="Direct Message", style="3", custom_id="btUpdate"),Button(label="Delete Messages", style="4", custom_id="btDelete")]
    embed=discord.Embed(title="ENTER YOUR USERNAME : ",url="https://www.instagram.com",description="")
    #embed.set_footer(text="https://www.google.com/?client=safari",icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3fwDfYfJoyfIsa5rKck0IMaF05qNPDsRt7Q&usqp=CAU")
    embed.add_field(name="aaaa",value="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3fwDfYfJoyfIsa5rKck0IMaF05qNPDsRt7Q&usqp=CAU",inline=False)
    await ctx.send(embed=embed)

   #url="https://scontent.cdninstagram.com/v/t50.16885-16/275268746_4831225750302025_2630281466842630322_n.mp4?_nc_ht=instagram.fcdg1-1.fna.fbcdn.net&_nc_cat=101&_nc_ohc=J8uZDQrng3oAX_iQzHY&edm=APU89FABAAAA&ccb=7-4&oe=62248AC0&oh=00_AT8jqfsNaXcqKql5e75uANpd8r82_4NuKfj27YIuzPOvjA&_nc_sid=86f79a%27,%20scheme=%27https%27,%20host=%27instagram.fcdg1-1.fna.fbcdn.net%27,%20tld=%27net%27,%20host_type=%27domain%27,%20port=%27443%27,%20path=%27/v/t50.16885-16/275268746_4831225750302025_2630281466842630322_n.mp4%27,%20query=%27_nc_ht=instagram.fcdg1-1.fna.fbcdn.net&_nc_cat=101&_nc_ohc=J8uZDQrng3oAX_iQzHY&edm=APU89FABAAAA&ccb=7-4&oe=62248AC0&oh=00_AT8jqfsNaXcqKql5e75uANpd8r82_4NuKfj27YIuzPOvjA&_nc_sid=86f79a"
    url="https://upload.wikimedia.org/wikipedia/commons/2/2c/Rotating_earth_%28large%29.gif"
    #url = (VideoFileClip(url))
    contents = urllib2.urlopen(url).read()
    #contents= BytesIO(contents)
    name="img"
    image_file = discord.File(BytesIO(contents),filename=f"{name}.gif")
    await ctx.send(file=image_file )

    #url="https://upload.wikimedia.org/wikipedia/commons/2/2c/Rotating_earth_%28large%29.gif"
    embed=discord.Embed(title="ENTER YOUR USERNAME : ",url="https://www.instagram.com",description="")
    embed.set_image(url="attachment://img.gif.")
    await ctx.send(embed=embed)
    #await ctx.channel.send(clip.filename)
    a=1
    #await ctx.send(file=discord.File(fp= contents, filename='test.gif'))






@client.command()
async def begin(ctx):
    #await ctx.guild.create_category_channel("Reseaux Sociaux")
    channelToCreate=listChannels
    
    for i in range(len(channelToCreate)):
        await ctx.guild.create_text_channel(channelToCreate[i],position=i)
    existing_channel = discord.utils.get(ctx.guild.channels).guild.channels
    buttons = [Button(label="Sign in", style="1", custom_id="btSignIn"),Button(label="Delete channel", style="4", custom_id="btDeleteChan")]
    await Tools.createButton(ctx,channelToCreate,"Please sign in before using this channel",buttons,client)

@client.command()
async def stop(ctx):
    channelToDelete=listChannels
    existing_channel = discord.utils.get(ctx.guild.channels).guild.channels
    for i in range (len(channelToDelete)):
        for j in range (len(existing_channel)):
            if(channelToDelete[i] in existing_channel[j].name):
                await discord.utils.get(ctx.guild.channels, name=channelToDelete[i]).delete()
                break

@client.event
async def on_button_click(interaction):
    currentChannel=interaction.channel.name
    currentAction=interaction.component.label
    await interaction.channel.purge()  

    if(interaction.channel.name=="twitter"):
        if(currentAction=="Sign in"):
            await Twitter.SignInTwitter(ctx=interaction.channel,client=client)
        elif(currentAction=="Direct Message"):
            await Twitter.getUserMessages(ctx=interaction.channel)
        elif(currentAction=="Mentions"):
            await Twitter.getMentions(ctx=interaction.channel)
        await Tools.createButton(interaction.channel,[interaction.channel.name],"What do you want to do?",Twitter.ButtonsUpdates,client)
    
    
    elif(interaction.channel.name=="instagram"):
        if(currentAction=="Sign in"):
            try:
                await Instagram.SignInInstagram(ctx=interaction.channel,client=client)
            except:
                await Tools.createButton(interaction.channel,[interaction.channel.name],"Error, try again...",Instagram.ButtonsSignIn,client)
                return
        elif(currentAction=="Feed"):
            await Instagram.getFeedInstagram(ctx=interaction.channel)
     
        elif(currentAction=="Direct Message"):
            await Instagram.getUserMessages(ctx=interaction.channel)
        await Tools.createButton(interaction.channel,[interaction.channel.name],"What do you want to do?",Instagram.ButtonsUpdates,client)

    elif(interaction.channel.name=="messenger"):
        if(currentAction=="Sign in"):
            try:
                await Messenger2.SignInMessenger(ctx=interaction.channel,client=client)
            except:
                await Tools.createButton(interaction.channel,[interaction.channel.name],"Error, try again...",Instagram.ButtonsSignIn,client)
                return
        #elif(currentAction=="Direct Message"):
            #await Instagram.getUserMessages(ctx=interaction.channel)
        await Tools.createButton(interaction.channel,[interaction.channel.name],"What do you want to do?",Instagram.ButtonsUpdates,client)

@client.event
async def on_reaction_add(reaction, user):
    #if user != client.user:
    #    if str(reaction.emoji) == "???":
    #        await reaction.message.delete()
    
    if(user.display_name!="MessagesBot"):
        if(reaction.message.channel.name=="instagram"):
            Feed.currentIndex=Tools.manageIndexOnReaction(reaction,Feed.currentIndex,len(Feed.listPhoto))
            Instagram.setFeedEmbed()
            await Tools.manageEmbedReaction(Feed.messageEmbed,Feed.embed,reaction,user)

        elif(reaction.message.channel.name=="twitter"):
            UserMessages.currentMessageIndex =Tools.manageIndexOnReaction(reaction,UserMessages.currentMessageIndex,len(UserMessages.listUserID))
            await Twitter.setMessagesEmbed()
            await Tools.manageEmbedReaction(UserMessages.messageEmbed,UserMessages.embed,reaction,user)
     

@client.command()
async def send(ctx,*,message):
    if(len(ctx.message.mentions)>0):
        if(ctx.message.mentions[0].name=="MessagesBot"):
            if(ctx.channel.name=="twitter"):
                recipientID=Twitter.api.show_user(id=UserMessages.listUserID[UserMessages.currentMessageIndex])['id']
                event=Twitter.setJsonMessage(recipientID,message)
                Twitter.api.post('direct_messages/events/new', params=json.dumps(event))
                Twitter.api.update_status(in_reply_to_status_id=int(tweetByIDs.get(ctx.message.reference.message_id)[0]), status="@"+tweetByIDs.get(ctx.message.reference.message_id)[1]+" "+message)
            elif(ctx.channel.name=="instagram"):
                await Instagram.replyMessage(message)
    else:
        if(ctx.channel.name=="twitter"):
            Twitter.api.update_status(status=message,auto_populate_reply_metadata=True)

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



