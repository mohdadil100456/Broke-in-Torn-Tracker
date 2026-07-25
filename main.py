import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TORN_API_KEY = os.getenv("TORN_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Game(name="Tracking Torn City")
    )

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def player(ctx, player_id: int):
    url = f"https://api.torn.com/user/{player_id}?selections=profile&key={TORN_API_KEY}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    if "error" in data:
        await ctx.send("❌ Invalid Torn API key or Player ID.")
        return

    embed = discord.Embed(
        title=data["name"],
        color=discord.Color.blue()
    )

    embed.add_field(name="Level", value=data["level"])
    embed.add_field(name="Rank", value=data["rank"])
    embed.add_field(name="Status", value=data["status"]["description"])

    await ctx.send(embed=embed)

bot.run(TOKEN)