import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="Broke in Torn Tracker",
            description="Available Commands",
            color=discord.Color.blue()
        )

        embed.add_field(name="!ping", value="Check if the bot is online.", inline=False)
        embed.add_field(name="!player <id>", value="Look up a Torn player.", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))