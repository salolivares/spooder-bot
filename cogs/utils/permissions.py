from discord.ext import commands

def checkIfOwner(message):
	return message.author.id == '140350353521639424'

def isOwner():
	return commands.check(lambda ctx: checkIfOwner(ctx.message))