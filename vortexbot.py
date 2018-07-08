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
commands_channel_id = str(os.environ.get("COMMANDS_CHANNEL_ID"))
droplobby_channel_id = str(os.environ.get("DROPLOBBY_CHANNEL_ID"))

status_message_objects = []
drop_active = False

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
	
	global drop_active
	global status_message_objects
	
	droplobby_channel_object = bot.get_server(vortex_server_id).get_channel(droplobby_channel_id)
	
	if message.content == "ping":
		await bot.send_message(message.channel, "pong")
	
	
	status_ask = False
	for status_command in status_commands:
		if status_command.lower() in message.content.lower():
			status_ask = True
			
	if message.author.id != bot.user.id:
		if message.server.id == vortex_server_id:
			if message.channel.id == commands_channel_id:
				if (message.content[:11] == "!drop start") or (message.content[:6] == "!start"):
					if not drop_active:
						await bot.send_message(droplobby_channel_object, "@here")
						embed=discord.Embed(title="**Drop lobby started!**", color=0x62f400)
						embed.add_field(name="To Join: ", value="-Add my SocialClub: **VORTEXDP**", inline=False)
						status_message_objects.append(await bot.send_message(droplobby_channel_object, embed=embed))
						
						drop_active = True
					else:
						await bot.send_message(message.channel, "**A drop is already happening.**")
						
						
						
				elif (message.content[:10] == "!drop stop") or (message.content[:9] == "!drop end") or (message.content[:5] == "!stop"):
					if drop_active:
						for status_message_object in status_message_objects:
							embed=discord.Embed(title="**Drop lobby started!**", color=0x62f400)
							embed.add_field(name="To Join: ", value="-Add my SocialClub!", inline=False)
							await bot.edit_message(status_message_object, embed=embed)
						status_message_objects = []
						embed=discord.Embed(title="**Drop lobby over!**", description="If you didnt get to join, stay tuned for the next one!", color=0xff060d)
						await bot.send_message(droplobby_channel_object, " @here")
						await bot.send_message(droplobby_channel_object, embed=embed)
						drop_active = False
					else:
						await bot.send_message(message.channel, "**There is no current drop happening.**")
		
		
		
			if (message.content[:7] == "!status") or (message.content[:12] == "!drop status") or (status_ask):
				if drop_active:
					embed=discord.Embed(title="**Drop lobby currently active!**", color=0x1cc104)
					embed.add_field(name="To Join: ", value="-Add my SocialClub: **VORTEXDP**", inline=False)
					status_message_objects.append(await bot.send_message(message.channel, embed=embed))
				else:
					embed=discord.Embed(title="**Drop lobby not active!**", description="Next one coming soon!", color=0xff060d)
					await bot.send_message(message.channel, embed=embed)
	
bot.run(token)
