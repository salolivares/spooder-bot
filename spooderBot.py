import discord
import random
import logging
import asyncio
import json
from cleverbot import Cleverbot

logging.basicConfig(level=logging.INFO)
client = discord.Client()
cb = Cleverbot()

description = "Batman was right. Babies aren't fireproof. -Spidey"

# Commands
commands = {
	'!ask':'Ask spidey a question',
	'!boom':'Not implemented',
	'!overwatchparty':'[Not implemented] Randomly select an overwatch party and heroes from at random',
	'!votekick':'[Not implemented] Annoying discord member? Kick him to the tune of the mw2 nuke sequence',
	'!help':"Ask for help"
}

@client.event
async def on_ready():
	print('------')
	print(client.user.name + " is now Online")
	print('------')
	servers = str(len(client.servers))
	channels = str(len([c for c in client.get_all_channels()]))
	print("Connected to:")
	print(servers + " servers")
	print(channels + " channels")
	print('------')

async def boom():
	await client.wait_until_ready()
	voiceChannel = None
	for server in client.servers:
		for channel in server.channels:
			if channel.name == 'General':
				voiceChannel = channel
	voiceClip = await client.join_voice_channel(voiceChannel)
	player = voiceClip.create_ffmpeg_player('boomheadshot.mp3')
	player.start()

async def cleverBot(question, channel):
	if not question:
		return await client.send_message(channel, "Please ask me a question")
	await client.send_message(channel, cb.ask(question))

async def help(channel, author):
	response = description + "\n\n"
	for i in commands:
		response += i + " " + commands[i] + "\n\n"
	return await client.send_message(channel, str(author.mention) + codeBlock(response))

@client.event
async def on_message(message):
	# send reply on dat boi
	if "dat boi" in message.content:
		await client.send_message(message.channel, "oh shit wadd up", tts = True)
	# help function
	elif message.content.startswith("!help"):
		await help(message.channel, message.author)
	# prepare for cleverbot response
	elif message.content.startswith("!ask"):
		await cleverBot(" ".join(message.content.split()[1:]), message.channel)

def load_credentials():
	with open('credentials.json') as f:
		return json.load(f)

def codeBlock(s):
	return "```" + s + "```"

if __name__ == '__main__':
	credentials = load_credentials()
	client.run(credentials['token'])