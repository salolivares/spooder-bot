import datetime
import traceback

import sys
from discord.ext import commands
import logging
import json

description = "I am bot written by Sal. My purpose is to do dope sh*t."

# Bot extensions
startup_extensions = [
    "cogs.fun",
    "cogs.rng",
    "cogs.music",
    "cogs.soundboard",
    "cogs.admin"
]

bot = commands.Bot(command_prefix='!', description=description)

# Logging setup
discordLogger = logging.getLogger('discord')
discordLogger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='spooderbot.log', encoding='utf-8', mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)


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
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()


@bot.event
async def on_command(command, ctx):
    message = ctx.message
    destination = None
    if message.channel.is_private:
        destination = 'Private Message'
    else:
        destination = '#{0.channel.name} ({0.server.name})'.format(message)

    logger.info('{0.author.name} in {1}: {0.content}'.format(message, destination))


@bot.event
async def on_message(message):
    # don't want any infinite loops do we?
    if message.author.bot:
        return

    # dat boi
    if "dat" in message.content and "boi" in message.content:
        return await bot.send_message(message.channel, "oh shit wadd up", tts=True)

    await bot.process_commands(message)


@bot.event
async def on_resumed():
    print('Resumed...')


def load_credentials():
    with open('resources/credentials.json') as f:
        return json.load(f)


if __name__ == '__main__':
    credentials = load_credentials()
    logger.info("Loaded Credentials")

    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            logger.error('Failed to load extension {}. {}: {}'.format(extension, type(e).__name__, e))

    bot.run(credentials['token'])