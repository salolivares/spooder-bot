import asyncio
import unicodedata

import re
from discord.ext import commands

from cogs.utils import permissions


class TimeParser:
    def __init__(self, argument):
        compiled = re.compile(r"(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?")
        self.original = argument
        try:
            self.seconds = int(argument)
        except ValueError as e:
            match = compiled.match(argument)
            if match is None or not match.group(0):
                raise commands.BadArgument('Failed to parse time.') from e

            self.seconds = 0
            hours = match.group('hours')
            if hours is not None:
                self.seconds += int(hours) * 3600
            minutes = match.group('minutes')
            if minutes is not None:
                self.seconds += int(minutes) * 60
            seconds = match.group('seconds')
            if seconds is not None:
                self.seconds += int(seconds)

        if self.seconds < 0:
            raise commands.BadArgument('I don\'t do negative time.')


class Utilities:
    """Provides bot info, statistics, and other misc things"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def hello(self):
        """Display a hello message"""
        await self.bot.say("Howdy.")

    @commands.command(hidden=True)
    @permissions.isOwner()
    async def charinfo(self, *, characters: str):
        """Shows info on a the characters passed in"""

        if len(characters) > 12:
            await self.bot.say('Too many characters ({}/12)'.format(len(characters)))
            return

        def to_string(c):
            digit = format(ord(c), 'x')
            name = unicodedata.name(c, 'Name not found.')
            return '0x{0}: {1} - {2} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{0}>'.format(digit, name,
                                                                                                            c)

        await self.bot.say('\n'.join(map(to_string, characters)))

    @commands.command(pass_context=True, aliases=['reminder', 'remind'])
    async def timer(self, ctx, time: TimeParser, *, message=''):
        """Reminds you of something after a certain amount of time.
        The time can optionally be specified with units such as 'h'
        for hours, 'm' for minutes and 's' for seconds. If no unit
        is given then it is assumed to be seconds. You can also combine
        multiple units together, e.g. 2h4m10s.
        """

        author = ctx.message.author
        reminder = None
        completed = None

        if not message:
            reminder = 'Alright {0.mention}, I\'ll remind everyone in {1.seconds} seconds.'
            completed = 'Listen up @everyone, {0.name} asked everyone to be reminded about something.'
        else:
            reminder = 'Alright {0.mention}, I\'ll remind everyone about "{2}" in {1.seconds} seconds.'
            completed = 'Listen up @everyone, {0.name} asked you guys to be reminded about "{1}".'

        await self.bot.say(reminder.format(author, time, message))
        await asyncio.sleep(time.seconds)
        await self.bot.say(completed.format(author, message))

    @timer.error
    async def timer_error(self, error, ctx):
        if type(error) is commands.BadArgument:
            await self.bot.say(str(error))


def setup(bot):
    bot.add_cog(Utilities(bot))
