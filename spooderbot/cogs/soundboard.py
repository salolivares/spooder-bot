import os, random
import discord
from discord.ext import commands

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')


class SoundBoard:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def boom(self, ctx):
        """BOOOOOM! HEADSHOT!"""
        try:
            voice = await self.bot.join_voice_channel(ctx.message.author.voice_channel)
            player = voice.create_ffmpeg_player("resources/sounds/boom.mp3")
            player.start()
        except:
            pass

        while True:
            try:
                if player.is_done():
                    await voice.disconnect()
                    break
            except:
                break

    @commands.command(pass_context=True, no_pm=True)
    async def cena(self, ctx):
        '''AND HIS NAME IS JOHN CENAAAA'''
        try:
            voice = await self.bot.join_voice_channel(ctx.message.author.voice_channel)
            player = voice.create_ffmpeg_player("resources/sounds/cena/" + random.choice(os.listdir("resources/sounds/cena")))
            player.start()
        except:
            pass

        while True:
            try:
                if player.is_done():
                    await voice.disconnect()
                    break
            except:
                break


def setup(bot):
    bot.add_cog(SoundBoard(bot))
    print("Soundboard cog loaded.")
