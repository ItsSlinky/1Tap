import discord
from pymongo import MongoClient
from discord.ext import commands
from discord.ext.commands import has_permissions

key = "vafPZVTskh5FDGI5"

cluster = MongoClient(f"mongodb+srv://disnitro:{key}@cluster0.juv3x.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["1Tap"]
channelsdb = db["channels"]

class messageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        elif message.channel.id == channelsdb.find_one({"_id": message.guild.id})["channel"]:
            await message.delete()

            results = channelsdb.find({})

            for result in results:
                webhookid = result["webhook"]
                channelid = result["channel"]

                webhook = await self.bot.fetch_webhook(webhookid)
                await webhook.edit(name="1Tap")

                if message.attachments:
                    for attachment in message.attachments:
                        if message.content == "":
                            messageembed = discord.Embed(colour=discord.Colour(0xFF0000))

                            messageembed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=f"{message.author.avatar}")
                            messageembed.set_image(url=f"{attachment.url}")
                            messageembed.set_footer(text=f"{message.guild.name} | 1Tap")

                            await webhook.send(embed=messageembed, avatar_url="https://cdn.discordapp.com/attachments/962783546219585616/966662273793933382/logo.png") 
                        else:
                            messageembed = discord.Embed(description=f"{message.content}", colour=discord.Colour(0xFF0000))

                            messageembed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=f"{message.author.avatar}")
                            messageembed.set_thumbnail(url=f"{attachment.url}")
                            messageembed.set_footer(text=f"{message.guild.name} | 1Tap")

                            await webhook.send(embed=messageembed, avatar_url="https://cdn.discordapp.com/attachments/962783546219585616/966662273793933382/logo.png") 
                else:
                    messageembed = discord.Embed(description=f"{message.content}", colour=discord.Colour(0xFF0000))

                    messageembed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=f"{message.author.avatar}")
                    messageembed.set_footer(text=f"{message.guild.name} | 1Tap")

                    await webhook.send(embed=messageembed, avatar_url="https://cdn.discordapp.com/attachments/962783546219585616/966662273793933382/logo.png") 
        else:
            return

def setup(bot):
    bot.add_cog(messageEvent(bot))
