# BWUBot version 2.0 by GaMeNu
# I will attempt to document my code better this time around

# imports
import asyncio
# Make SURE the file "bot_cmds.py" is in the same directory as this file!
from bot_cmds import Run
import discord
from discord import app_commands
from dotenv import load_dotenv
import json
import logging
import os
import time as t

# env vars
load_dotenv()
TOKEN = os.getenv('BWU_DISCORD_TOKEN')
GUILD = int(os.getenv('DISCORD_GUILD'))
COMM_CHANNEL = int(os.getenv('DF_COMMUNICATION_CHANNEL'))
BOTDATA = os.getenv('GD_STORAGE_PATH')
VERSION = os.getenv('VERSION')

# bot setup
bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)
guild = discord.utils.find(lambda g: g.id == GUILD, bot.guilds)
comm_channel: discord.TextChannel = bot.get_channel(COMM_CHANNEL)

logger = logging.Logger(name='BWUBot',level=logging.INFO)
logger.setLevel(logging.DEBUG)



try:
    with open(BOTDATA, 'r') as f:
        temp_store = json.loads(f.read())
except:
    with open(BOTDATA, 'w') as f:
        f.write(json.dumps({}))


async def syncCMDs(channel: discord.TextChannel):

    # Iterate on every message in channel history, get all commands, and send them. Then delete the original message.
    # P A I N

    messages = channel.history()

    logger.info('Started syncing all messages in communication channel')
    print('Started syncing all messages in communcation channel')
    async for message in messages:
        content = message.content.replace('\n', '').split(';')

        # iterate on every command, make sure is not a comment
        if (not message.content.startswith('#!')):
            for command in content:
                if command != '' and command[0] != '#':
                    await Run.run_command(command)
            
            await message.delete()
        
        await asyncio.sleep(0.1)


# Command to sync all previously sent msgs
@tree.command(name='sync', description='Manually sync all messages in channel')
async def sync(intr: discord.Interaction):
    # Make sure this is the correct channel
    if (intr.channel.id != COMM_CHANNEL):
        await intr.response.send_message('Error: Incorrect channel! Please use this command in <#1062285172378185799> instead!')
        return

    await intr.response.defer()
    await intr.channel.send('#! Begun syncing!', delete_after=3)
    await syncCMDs(intr.channel)
    await intr.channel.send('#! Done syncing!', delete_after=3)

# on_ready event,


@bot.event
async def on_ready():
    global guild
    global comm_channel
    comm_channel = bot.get_channel(COMM_CHANNEL)

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='the world burn because of me.'), status=discord.Status.dnd)
    await tree.sync(guild=guild)

    #Sync on online
    await comm_channel.send('#! Begun syncing!', delete_after=3)
    await syncCMDs(comm_channel)
    await comm_channel.send('#! Done syncing!', delete_after=3)


@bot.event
async def on_message(msg: discord.Message):
    if msg.channel.id == COMM_CHANNEL and msg.author != bot.user:
        await syncCMDs(msg.channel)


print(f'Welcome, and thank you for using BWUBot version 2!')
print(f'BWUBot version {VERSION}')
print(f'Made by GaMeNu')
print('WARNING: This is not yet ready as a functional piece! Please do not run this as the Grief Detector!')
bot.run(TOKEN)