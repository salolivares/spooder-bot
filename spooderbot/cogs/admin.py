from discord.ext import commands

from cogs.utils import permissions


class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.database

    @commands.group(pass_context=True, no_pm=True)
    @permissions.isOwner()
    async def ignore(self, ctx):
        """Handles ignore list. Anything on the ignore list is barred from using commands."""
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @ignore.command(name='list', pass_context=True)
    async def ignoreList(self, ctx):
        """List which channels and users are being ignored."""
        channels = self.db.getIgnoredChannels()
        users = self.db.getIgnoredUsers()

        message = "Ignored Channels\n------------------\n"

        if channels:
            message += ('\n'.join(channels))
        else:
            message += "None\n"

        message += "Ignored Users\n--------------------"
        if users:
            message += '\n'.join(self.db.getIgnoredUsers())
        else:
            message += "None\n"


def setup(bot):
    bot.add_cog(Admin(bot))
