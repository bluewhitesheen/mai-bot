import discord
import json #o
import os #o
from dotenv import load_dotenv
from discord.ext import commands
from mai_bot.find_song import find_songs_by_keyword
from mai_bot.choujoukyuu import MasterChoujoukyuu
from mai_bot.randomsong import random_song
from mai_bot.note_designer import find_nd
from mai_bot.note_designer_songs import find_nds

# 載入環境變數
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user}")

@bot.command(aliases=["f"])
async def find(ctx, *, keyword: str):
    results = find_songs_by_keyword(keyword)
    await ctx.reply("\n\n".join(results))

@bot.command()
async def 超上級(ctx):
    results = MasterChoujoukyuu()
    await ctx.reply("\n".join(results))

@bot.command()
async def random(ctx):
    results = random_song()
    await ctx.reply(results)

# 找譜師
@bot.command()
async def nd(ctx, *, keyword: str):
    results = find_nd(keyword)
    await ctx.reply("\n".join(results))

# 列出譜師和歌曲資訊
@bot.command()
async def nds(ctx, *, keyword: str):
    results = find_nds(keyword)
    await ctx.reply("\n".join(results))

# ctx 範例
@bot.command()
async def greet(ctx):
    await ctx.send(f"你好 {ctx.author.mention}！這是 {ctx.channel.name} 頻道")

# 記得在 .env 或 config.py 中妥善保存 TOKEN
bot.run(TOKEN)
