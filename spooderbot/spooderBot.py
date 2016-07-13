import discord
from discord.ext import commands
from cogs.utils import permissions
import random
import logging
import asyncio
import json

description = "Batman was right. Babies aren't fireproof. - Spidey"

# Bot extensions
startup_extensions = [
	"cogs.fun",
	"cogs.rng",
	"cogs.music",
	"cogs.soundboard"
]

bot = commands.Bot(command_prefix='!', description=description)

# Logging setup
logging.basicConfig(level=logging.INFO)

@bot.event
async def on_ready():
	print('------')
	print(bot.user.name + " is now Online")
	print('------')
	servers = str(len(bot.servers))
	channels = str(len([c for c in bot.get_all_channels()]))
	print("Connected to:")
	print(servers + " servers")
	print(channels + " channels")
	print('------')

@bot.event
async def on_message(message):
	# don't want any infinite loops do we?
	if message.author == bot.user:
		return

	# dat boi
	if "dat" in message.content and "boi" in message.content:
		return await bot.send_message(message.channel, "oh shit wadd up", tts = True)

	await bot.process_commands(message)

@bot.command(hidden=True)
@permissions.isOwner()
async def load(*, module : str):
	"""Loads a module."""
	module = module.strip()
	try:
		bot.load_extension(module)
	except Exception as e:
		await bot.say('\U0001f52b')
		await bot.say('{}: {}'.format(type(e).__name__, e))
	else:
		await bot.say('\U0001f44c')

@bot.command(hidden=True)
@permissions.isOwner()
async def unload(*, module : str):
	"""Unloads a module."""
	module = module.strip()
	try:
		bot.unload_extension(module)
	except Exception as e:
		await bot.say('\U0001f52b')
		await bot.say('{}: {}'.format(type(e).__name__, e))
	else:
		await bot.say('\U0001f44c')

@bot.command(pass_context=True, hidden=True)
@permissions.isOwner()
async def debug(ctx, *, code : str):
	"""Evaluates code."""
	code = code.strip('` ')
	python = '```py\n{}\n```'
	result = None

	try:
		result = eval(code)
	except Exception as e:
		await bot.say(python.format(type(e).__name__ + ': ' + str(e)))
		return

	if asyncio.iscoroutine(result):
		result = await result

	await bot.say(python.format(result))

def load_credentials():
	with open('credentials.json') as f:
		return json.load(f)

if __name__ == '__main__':
	credentials = load_credentials()

	for extension in startup_extensions:
		try:
			bot.load_extension(extension)
		except Exception as e:
			print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

	bot.run(credentials['token'])