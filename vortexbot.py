import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os

token = str(os.environ.get("BOT_TOKEN"))
vortex_server_id = str(os.environ.get("VORTEX_SERVER_ID"))
socialclub_name = str(os.environ.get("SOCIALCLUB_NAME"))

welcome_channel_id = str(os.environ.get("WELCOME_CHANNEL_ID"))
rules_channel_id = str(os.environ.get("RULES_CHANNEL_ID"))
announcements_channel_id = str(os.environ.get("ANNOUNCEMENTS_CHANNEL_ID"))
commands_channel_id = str(os.environ.get("COMMANDS_CHANNEL_ID"))
droplobby_channel_id = str(os.environ.get("DROPLOBBY_CHANNEL_ID"))
logs_channel_id = str(os.environ.get("LOGS_CHANNEL_ID"))
games_channel_id = str(os.environ.get("GAMES_CHANNEL_ID"))

gmt_plus = 2

game_not_active_str = "Drop Lobby NOT ACTIVE"
game_active_str = "Drop Lobby ACTIVE"

status_commands = [
"Lobby is over?", "still dropping?", "lobby lit?", "lobby active?", "Is there a lobby?", "is drop on?",
"lobby still going?", "there a drop now?", "still drop?", "is there drop?", "is there a drop?", "drop lobby on?"
]
status_message_objects = []
drop_active = False

destruction = False

Client = discord.Client()
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
	await bot.wait_until_ready()
	print (bot.user.name + " is ready")
	print ("ID: " + bot.user.id)
	
	await bot.change_presence(game=discord.Game(name=game_not_active_str))
	
@bot.event
async def on_member_join(member):
	
	welcome_channel_object = bot.get_server(vortex_server_id).get_channel(welcome_channel_id)
	rules_channel_object = bot.get_server(vortex_server_id).get_channel(rules_channel_id)
	announcements_channel_object = bot.get_server(vortex_server_id).get_channel(announcements_channel_id)
	
	await bot.send_message(welcome_channel_object, "Hello {0}, welcome to **Vortex Drops**. Make sure to read {1} and {2}!".format(member.mention, rules_channel_object.mention, announcements_channel_object.mention))
	
@bot.event
async def on_message(message):
	
	global socialclub_name
	
	global status_commands
	global drop_active
	global status_message_objects
	
	global destruction
	global member_hero
	
	
	droplobby_channel_object = bot.get_server(vortex_server_id).get_channel(droplobby_channel_id)
	logs_channel_object = bot.get_server(vortex_server_id).get_channel(logs_channel_id)
	games_channel_object = bot.get_server(vortex_server_id).get_channel(games_channel_id)
	
	message_time = str(int(str(message.timestamp)[11:13]) + gmt_plus) + str(message.timestamp)[13:19]
	message_date = "{0}/{1}/{2}".format(str(message.timestamp)[8:10], str(message.timestamp)[5:7], str(message.timestamp)[:4])
	
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
						embed.add_field(name="To Join: ", value="-Add my SocialClub: **{0}**".format(socialclub_name), inline=False)
						status_message_objects.append(await bot.send_message(droplobby_channel_object, embed=embed))
						
						await bot.change_presence(game=discord.Game(name=game_active_str))
						
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
						
						await bot.change_presence(game=discord.Game(name=game_not_active_str))
						
						drop_active = False
					else:
						await bot.send_message(message.channel, "**There is no current drop happening.**")
		
		
		
				elif message.content[:12] == "!destruction":
					destruction = True
					starting_spaces = 50
					for x in range(5):
						x += 1
						if x == 1:
							message_to_edit = await bot.send_message(games_channel_object, ":scream: :house: :house: :house: :house: :house:{0}:bomb::smiling_imp:".format((starting_spaces-10)*" "))
						else:
							for y in range(1):
								await asyncio.sleep(1)
								if not destruction:
									break
							if destruction:
								await bot.edit_message(message_to_edit, ":scream: :house: :house: :house: :house: :house:{0}:bomb:{1}:smiling_imp:".format((starting_spaces-(x*10))*" ", ((x-1)*10)*" "))
							else:
								await bot.edit_message(message_to_edit, ":sweat_smile: :house: :house: :house: :house: :house:{0}:imp:".format((starting_spaces)*" "))
								await bot.send_message(games_channel_object, "**{0} saved the town! :thumbsup:**".format(member_hero.name))
								break
					if destruction:
						await asyncio.sleep(0.2)
						await bot.edit_message(message_to_edit, ":fire: :fire: :fire: :fire: :fire: :fire:{0}:smiling_imp:".format(starting_spaces*" "))
						await asyncio.sleep(0.2)
						await bot.edit_message(message_to_edit, ":dizzy_face: :house_abandoned: :house_abandoned: :house_abandoned: :house_abandoned: :house_abandoned:{0}:smiling_imp:".format(starting_spaces*" "))

		
		
		
		
			if (message.content[:7] == "!status") or (message.content[:12] == "!drop status") or (status_ask):
				if drop_active:
					embed=discord.Embed(title="**Drop lobby currently active!**", color=0x1cc104)
					embed.add_field(name="To Join: ", value="-Add my SocialClub: **{0}**".format(socialclub_name), inline=False)
					status_message_objects.append(await bot.send_message(message.channel, embed=embed))
				else:
					embed=discord.Embed(title="**Drop lobby not active!**", description="Next one coming soon!", color=0xff060d)
					await bot.send_message(message.channel, embed=embed)
	
	
	
			elif message.content[:7] == "!donate":
				embed=discord.Embed(title="Donate Link", url="https://www.paypal.me/vortexdrops", description="Feel free to donate! Any amount would help.", color=0x154eb5)
				await bot.send_message(message.author, embed=embed)
				
				
				embed=discord.Embed(title="**{0} sent a donate request!**".format(message.author.display_name), color=0x154eb5)
				embed.set_author(name="{0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
				embed.set_footer(text="{0} @ {1}".format(message_date, message_time))
				await bot.send_message(logs_channel_object, embed=embed)
				
			
			
			elif message.content[:5] == "!save":
				if destruction:
					destruction = False
					member_hero = message.author
	
bot.run(token)
