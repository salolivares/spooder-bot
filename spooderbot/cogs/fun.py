import discord
from discord.ext import commands
from cleverbot import Cleverbot

class Fun():
	"""Random collection of 'fun' commands"""
	def __init__(self, bot):
		self.bot = bot
		self.cb = Cleverbot()

	@commands.command(description='Ask spooder bot a question')
	async def ask(self, *question : str):
		"""Ask the wise spooder a question"""
		# discord passes question as an array so combine the question array back into a string.
		question = ' '.join(question)
		if not question:
			return await self.bot.say("Ask me a question")
		try:
			return await self.bot.say(self.cb.ask(question))
		except Exception as e:
			print('Cleverbot failed\n{}: {}'.format(type(e).__name__, e))
			return await self.bot.say("Sorry, I can't answer any questions at the moment")

def setup(bot):
	bot.add_cog(Fun(bot))