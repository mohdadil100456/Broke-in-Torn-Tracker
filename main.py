import os
import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TORN_API_KEY = os.getenv("TORN_API_KEY")

# Set up Bot Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Game(name="Tracking Torn City")
    )

# Ping Command
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# Torn Player Lookup Command
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
                title=f"Profile: {data.get('name')} [{data.get('player_id')}]",
                color=discord.Color.blue()
            )
            embed.add_field(name="Level", value=data.get("level", "N/A"), inline=True)
            embed.add_field(name="Status", value=data.get("status", {}).get("description", "N/A"), inline=True)
            embed.add_field(name="Rank", value=data.get("rank", "N/A"), inline=False)
            
            await ctx.send(embed=embed)

# Start Bot Execution
if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_TOKEN is missing in your .env file!")
    else:
        bot.run(TOKEN)
