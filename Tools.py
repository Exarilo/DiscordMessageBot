import discord
from fpdf import FPDF
from pickle import TRUE
from io import BytesIO

class Tools:
    async def createButton(ctx,listChannels,message,listButtons,client):
        
        channelToCreate=listChannels
        existing_channel = discord.utils.get(ctx.guild.channels).guild.channels
        for j in range (len(channelToCreate)):
            for k in range (len(existing_channel)):
                if(channelToCreate[j] in existing_channel[k].name):
                    await ctx.guild.channels[k].send(message,components = listButtons)
        while True:
            interaction = await client.wait_for("button_click")



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


    async def manageEmbedReaction(message,embed,reaction, user):
        await message.remove_reaction(reaction, user)
        await message.edit(embed=embed)
        await message.add_reaction('◀️')
        await message.add_reaction('▶️') 

    def  manageIndexOnReaction(reaction,index,maxIndex):
        if str(reaction.emoji) == "◀️":
            index-=1
            if(index<0):
                index=maxIndex-1
        if str(reaction.emoji) == "▶️":      
            index+=1
            if(index==maxIndex):
                index=0
        return index
                
