from discord.ext import commands


class Mod:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.database

def setup(bot):
    bot.add_cog(Mod(bot))