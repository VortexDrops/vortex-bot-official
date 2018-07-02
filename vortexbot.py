import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os

token = str(os.environ.get("BOT_TOKEN"))
vortex_server_id = str(os.environ.get("VORTEX_SERVER_ID"))

welcome_channel_id = str(os.environ.get("WELCOME_CHANNEL_ID"))


Client = discord.Client()
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
	await bot.wait_until_ready()
	print (bot.user.name + " is ready")
	print ("ID: " + bot.user.id)
	
@bot.event
async def on_member_join(member):
	
	welcome_channel_object = bot.get_server(vortex_server_id).get_channel(welcome_channel_id)
	
	await bot.send_message(welcome_channel_object, "Hello {0}, welcome to **Vortex Drops**. Make sure to read #rules and #announcements!".format(member.mention))
	
bot.run(token)
