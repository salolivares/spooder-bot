import datetime

from discord.ext import commands
import discord
import logging
import logging.handlers
import json
import sys


from cogs.utils.database import Database

description = "I am bot written by Sal. My purpose is to do dope sh*t."

# Bot extensions
startup_extensions = [
    "cogs.fun",
    "cogs.rng",
    "cogs.music",
    "cogs.soundboard",
    "cogs.developer",
    "cogs.meta",
    "cogs.admin"
]

bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')


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
    print("Use this url to bring your bot to a server:")
    url = await get_oauth_url()
    bot.oauth_url = url
    print(url)
    print("------")


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

async def get_oauth_url():
    try:
        data = await bot.application_info()
    except AttributeError:
        return "Your discord.py is outdated. Couldn't retrieve invite link."
    return discord.utils.oauth_url(data.id)


def load_credentials():
    with open('resources/credentials.json') as f:
        return json.load(f)


def setup_logger():
    global logger

    logger = logging.getLogger("discord")
    logger.setLevel(logging.WARNING)
    handler = logging.FileHandler(filename='data/spooderbot/discord.log', encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
        '%(message)s',
        datefmt="[%d/%m/%Y %H:%M]"))
    logger.addHandler(handler)

    logger = logging.getLogger("spooderBot")
    logger.setLevel(logging.INFO)

    spooderbot_format = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
        '%(message)s',
        datefmt="[%d/%m/%Y %H:%M]")

    # setup STDOUT handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(spooderbot_format)
    stdout_handler.setLevel(logging.INFO)

    # setup file handler
    fhandler = logging.handlers.RotatingFileHandler(
        filename='data/spooderbot/spooderbot.log', encoding='utf-8', mode='a',
        maxBytes=10 ** 7, backupCount=5)
    fhandler.setFormatter(spooderbot_format)

    logger.addHandler(fhandler)
    logger.addHandler(stdout_handler)


if __name__ == '__main__':
    # Setup logger
    setup_logger()

    # Load credentials to log into discord
    credentials = load_credentials()
    logger.info("Loaded credentials from json")

    # Initialize database
    bot.database = Database()
    logger.info("Database initialized")


    # Load extensions
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            logger.info("Loaded {} cog".format(extension))
        except Exception as e:
            logger.warn('Failed to load extension {}. {}: {}'.format(extension, type(e).__name__, e))

    logger.info("spooderBot now running!")
    bot.client_id = credentials['client_id']
    bot.run(credentials['token'])
