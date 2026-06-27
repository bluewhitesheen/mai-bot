import discord
from dotenv import load_dotenv
from discord.ext import commands

from mai_bot.find_song import find_songs_by_keyword
from mai_bot.choujoukyuu import MasterChoujoukyuu
from mai_bot.randomsong import random_song
from mai_bot.note_designer import find_nd
from mai_bot.note_designer_songs import find_nds
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = bot


@bot.event
async def on_ready() -> None:
    print(f"{bot.user}")

# @client.event
# async def on_message(message) -> None:
#     print(f"message={message.content}")
#     await bot.process_commands(message)

@bot.command(aliases=["f"])
async def find(ctx, *, keyword: str) -> None:
    results = find_songs_by_keyword(keyword)
    await ctx.reply("\n\n".join(results))

@bot.command()
async def find_simple(ctx, *, keyword: str) -> None:
    results = find_songs_by_keyword(keyword)
    await ctx.reply("\n\n".join(results))


@bot.command(aliases=["fme"])
async def find_mas_exp(ctx, *, keyword: str) -> None:
    results = find_songs_by_keyword(
        keyword,
        difficulty_filter={"Re:MAS", "MAS", "EXP"},
    )
    await ctx.reply("\n\n".join(results))

@bot.command(aliases=["fm"])
async def find_mas(ctx, *, keyword: str) -> None:
    results = find_songs_by_keyword(
        keyword,
        difficulty_filter={"Re:MAS", "MAS"},
    )
    await ctx.reply("\n\n".join(results))


@bot.command(name="超上級", aliases=["choujoukyuu", "cj"])
async def choujoukyuu(ctx) -> None:
    results = MasterChoujoukyuu()
    await ctx.reply("\n".join(results))


@bot.command()
async def random(ctx) -> None:
    results = random_song()
    await ctx.reply(results)


@bot.command()
async def nd(ctx, *, keyword: str) -> None:
    results = find_nd(keyword)
    await ctx.reply("\n".join(results))


@bot.command()
async def nds(ctx, *, keyword: str) -> None:
    results = find_nds(keyword)
    await ctx.reply("\n".join(results))


@bot.command()
async def greet(ctx) -> None:
    await ctx.send(f"Hi {ctx.author.mention}, welcome to {ctx.channel.name}!")


bot.run(TOKEN)
