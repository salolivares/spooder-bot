import discord
from discord.ext import commands
import random
import logging
import asyncio
import json
from cleverbot import Cleverbot

description = "Batman was right. Babies aren't fireproof. -Spidey"

# Cogs
startup_extensions = [
]

bot = commands.Bot(command_prefix='!', description=description)
logging.basicConfig(level=logging.INFO)
cb = Cleverbot()

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
	if "dat boi" in message.content:
		return await bot.send_message(message.channel, "oh shit wadd up", tts = True)

	await bot.process_commands(message)

@bot.command(description='Ask spooder bot a question')
async def ask(*question : str):
	"""Ask the wise spooder a question"""
	question = ' '.join(question)
	if not question:
		return await bot.say("Ask me a question")
	return await bot.say(cb.ask(question))

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