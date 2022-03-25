import discord, functools
from discord.ext import commands
import os
import sys

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def eval(self, ctx, *, code):
        """Evaluates code"""
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self.bot._last_result,
        }

        env.update(globals())

        try:
            self.bot._last_result = eval(code, env)
            await ctx.send(f"```py\n{self.bot._last_result}\n```")
        except Exception as e:
            await ctx.send(f"```py\n{e}\n```")


def setup(bot):
    bot.add_cog(Owner(bot))
