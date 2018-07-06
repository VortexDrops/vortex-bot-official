import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os

token = str(os.environ.get("BOT_TOKEN"))
vortex_server_id = str(os.environ.get("VORTEX_SERVER_ID"))

welcome_channel_id = str(os.environ.get("WELCOME_CHANNEL_ID"))
rules_channel_id = str(os.environ.get("RULES_CHANNEL_ID"))
announcements_channel_id = str(os.environ.get("ANNOUNCEMENTS_CHANNEL_ID"))

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
	rules_channel_object = bot.get_server(vortex_server_id).get_channel(rules_channel_id)
	announcements_channel_object = bot.get_server(vortex_server_id).get_channel(announcements_channel_id)
	
	await bot.send_message(welcome_channel_object, "Hello {0}, welcome to **Vortex Drops**. Make sure to read {1} and {2}!".format(member.mention, rules_channel_object.mention, announcements_channel_object.mention))
	
@bot.event
async def on_message(message):
	if message.content == "sayhellobot":
		await bot.send_message(message.channel, "Hello, I'm alive")
	
bot.run(token)
