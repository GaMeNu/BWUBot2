# BWUBot version 2.0 by GaMeNu
# I will attempt to document my code better this time around

# imports
import asyncio
# Make SURE the file "bot_cmds.py" is in the same directory as this file!
import bot_cmds
import discord
from discord import app_commands
from dotenv import load_dotenv
import json
import logging
import math
import os
import time as t

# env vars
load_dotenv()
TOKEN = os.getenv('BWU_DISCORD_TOKEN')
GUILD = int(os.getenv('DISCORD_GUILD'))
COMM_CHANNEL = int(os.getenv('DF_COMMUNICATION_CHANNEL'))
OUT_CHANNEL = int(os.getenv('COMMAND_OUTPUT_CHANNEL'))
JSON_PATH = os.getenv('GD_STORAGE_PATH')
VERSION = os.getenv('VERSION')

# bot setup
bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)
guild = discord.utils.find(lambda g: g.id == GUILD, bot.guilds)
comm_channel: discord.TextChannel = bot.get_channel(COMM_CHANNEL)

logger = logging.Logger(name='BWUBot', level=logging.INFO)
logger.setLevel(logging.DEBUG)

temp_store = {}


def load_json_to_store():
    global temp_store

    try:
        with open(JSON_PATH, 'r') as f:
            temp_store = json.loads(f.read())

    except:
        logger.critical(
            f'ERROR: Cannot find storage file at path {JSON_PATH}!')

    else:
        logger.info(f'Successfully loaded JSON file from path {JSON_PATH}')


async def sync_commands(channel: discord.TextChannel):

    # Iterate on every message in channel history, get all commands, and send them. Then delete the original message.
    # P A I N

    messages = channel.history()

    logger.info('Started syncing all messages in communication channel')
    print('Started syncing all messages in communcation channel')
    async for message in messages:
        content = message.content.replace('\n', '').replace(' ', '').split(';')

        # iterate on every command, make sure is not a comment
        if (not message.content.startswith('#!')):
            for command in content:
                if command != '' and command[0] != '#':
                    # This one connection point, so much P A I N
                    await bot_cmds.run_command(command, bot)

            await message.delete()

        await asyncio.sleep(0.1)


# Command to sync all previously sent msgs
@tree.command(name='gd-sync', description='Manually sync all messages in channel')
async def gd_sync(intr: discord.Interaction):
    # Make sure this is the correct channel
    if (intr.channel.id != COMM_CHANNEL):
        await intr.response.send_message('Error: Incorrect channel! Please use this command in <#1062285172378185799> instead!')
        return

    await intr.response.send_message('#! Begun syncing!', ephemeral=True)
    await sync_commands(intr.channel)
    await intr.followup.send('#! Done syncing!', ephemeral=True)


@tree.command(name='gd-search', description='Search for a location to get the player that last placed a block in that location')
async def gd_search(intr: discord.Interaction, x: float, y: float, z: float):
    global temp_store
    loc = f'[{math.floor(x)},{math.floor(y)},{math.floor(z)}]'
    load_json_to_store()

    if not loc in temp_store.keys():
        await intr.response.send_message(f'There doesn\'t seem to be any player saved to location **{loc}**.')
    else:
        await intr.response.send_message(f'The last player to modify the block at location **{loc}** is **{temp_store[loc]}**')


# on_ready event,
@bot.event
async def on_ready():
    global guild
    global comm_channel
    comm_channel = bot.get_channel(COMM_CHANNEL)

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='the world burn because of me.'), status=discord.Status.dnd)
    await tree.sync(guild=guild)

    # Sync on online
    await comm_channel.send('#! Begun syncing!', delete_after=3)
    await sync_commands(comm_channel)
    await comm_channel.send('#! Done syncing!', delete_after=3)


@bot.event
async def on_message(msg: discord.Message):
    if msg.channel.id == COMM_CHANNEL and msg.author != bot.user:
        await sync_commands(msg.channel)


load_json_to_store()

print(f'Welcome, and thank you for using BWUBot version 2!')
print(f'BWUBot version {VERSION}')
print(f'Made by GaMeNu')
logger.warning(
    'WARNING: This is not yet ready as a functional piece! Please do not run this as the Grief Detector!')
bot.run(TOKEN)
