import discord
from discord.ext import commands

bot = commands.AutoShardedBot(shards=5, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

extentions = ["cogs.configCommands", "cogs.messageEvent"]

for ext in extentions:
    bot.load_extension(ext)
    print(f"{ext} has been loaded.")

bot.run("OTY1NzA1MDc3OTM3NTM3MDI0.Yl3E8A.kMTp59W4jFqi72ASkBMlL2uHwl0")