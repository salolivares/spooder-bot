import random
from discord.ext import commands


class RNG:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, *choices: str):
        """Chooses between multiple choices."""
        await self.bot.say(random.choice(choices))

    @commands.command()
    async def roll(self, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)

    @commands.command(description='A fine assortment of lenny faces', pass_context=True)
    async def lenny(self, ctx):
        """Displays a random lenny face."""
        lennyface = random.choice([
            "( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "ᕦ( ͡° ͜ʖ ͡°)ᕤ", "( ͡~ ͜ʖ ͡°)",
            "( ͡o ͜ʖ ͡o)", "͡(° ͜ʖ ͡ -)", "( ͡͡ ° ͜ ʖ ͡ °)﻿", "(ง ͠° ͟ل͜ ͡°)ง",
            "ヽ༼ຈل͜ຈ༽ﾉ"
        ])
        await self.bot.delete_message(ctx.message)
        await self.bot.say(lennyface)


def setup(bot):
    bot.add_cog(RNG(bot))
