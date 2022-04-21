import discord
from pymongo import MongoClient
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.commands import Option, SlashCommandGroup

key = "vafPZVTskh5FDGI5"

cluster = MongoClient(f"mongodb+srv://disnitro:{key}@cluster0.juv3x.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["1Tap"]
channelsdb = db["channels"]

class configCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    set = SlashCommandGroup("set", "Commands related to configuiring.")

    @set.command()
    @has_permissions(administrator=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the channel you want messages to come through."""
        if channelsdb.count_documents({"_id": ctx.guild.id}):
            results = channelsdb.update_one({"_id": ctx.guild.id})

            for result in results:
                channelid = result["channel"]

                if channelid == channel.id:
                    enabled = discord.Embed(colour=discord.Colour(0xe31809), description=f"{channel.name} is already set as the channel where messages come through.")

                    await ctx.respond(embed=enabled)
                else:
                    webhook = await channel.create_webhook(name="1Tap")
                    channelsdb.update_one({"_id": ctx.guild.id}, {"$set": {"channel": channel.id}})
                    channelsdb.update_one({"_id": ctx.guild.id}, {"$set": {"webhook": webhook.id}})

                    enabled = discord.Embed(colour=discord.Colour(0xe31809), description=f"{channel.name} has been set as the channel where messages come through.")

                    await ctx.respond(embed=enabled)
        else:
            webhook = await channel.create_webhook(name="1Tap")

            channelsdb.insert_one({"_id": ctx.guild.id, "channel": channel.id, "webhook": webhook.id})

            enabled = discord.Embed(colour=discord.Colour(0xe31809), description=f"{channel.name} has been set as the channel where messages come through.")

            await ctx.respond(embed=enabled)

def setup(bot):
    bot.add_cog(configCommands(bot))
