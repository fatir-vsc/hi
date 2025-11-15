#bot logic
import random

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>"
    password = ""

    for i in range(pass_length):
        password += random.choice(elements)

    return password

#main
import discord
import random
import time as t
import asyncio
from discord.ext import commands
from bot_logic import gen_pass

dictt = {"info" : "a command for another command info",
         "hello" : "a simple hello command",
         "heh" : "a command that says he multiple times",
         "password" : "a command that generates a random password",
         "joined" : "a command that tells you when a member joined",
         "roll" : "a command that rolls dice in NdN format",
         "reaction" : "a command that tests your reaction time(type 'stop' as fast as you can when prompted)"}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)

# Replace with your actual channel ID
CHANNEL_ID = 123456789012345678

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def password(ctx):
    await ctx.send("your password is:" + gen_pass(10))

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    # Joined at can be None in very bizarre cases so just handle that as well
    if member.joined_at is None:
        await ctx.send(f'{member} has no join date.')
    else:
        await ctx.send(f'{member} joined {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)
@bot.command()
async def reaction(ctx):
    """Tests your reaction time!"""
    await ctx.send("Get ready...")
    await asyncio.sleep(random.randint(2, 5))
    start = t.time()
    await ctx.send("Go!")
    
    def check(m):
        return m.author == ctx.author and m.content.lower() == "stop"
    
    try:
        await bot.wait_for('message', check=check, timeout=10.0)
        end = t.time()
        reaction_time = end - start
        await ctx.send(f'Your reaction time is {reaction_time:.3f} seconds!')
    except asyncio.TimeoutError:
        await ctx.send('You took too long to respond!')

@bot.command()
async def info(ctx, *, command_name: str):
    """Provides information about a specific command."""
    command_info = dictt.get(command_name.lower())
    if command_info:
        await ctx.send(f'Info about "{command_name}": {command_info}')
    elif command_name.lower() == "all":
        all_info = "\n".join([f"{cmd}: {desc}" for cmd, desc in dictt.items()])
        await ctx.send(f'All command info:\n{all_info}')
    else:
        await ctx.send(f'No information found for command "{command_name}".')
        
bot.run("ur token")
