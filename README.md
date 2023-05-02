# BWUBot2 - DEPRECATED
**This version of BWUBot has been deprecated! See the GDBot repository instead.**
This version is deprecated due to poor design, using a large JSON file. GDv3 will most likely use a relational database.

Version 2 of BWU bot, supporting more Plot to Discord integration and fully rewritten using discord.py 2.1's slash-commands

## .env setup:
```
BWU_DISCORD_TOKEN = <Discord bot token>
DISCORD_GUILD = <Your Discord server ID>
DF_COMMUNICATION_CHANNEL = <Your Discord communication channel ID (Where messages and webhooks will be sent to for the bot to read)>
COMMAND_OUTPUT_CHANNEL = <Your Discord command output channel. Messages FROM the bot will be sent here>

GD_STORAGE_PATH = <Path to json storage file on your computer>/gd_storage.json

VERSION = 2.0.0 - 0.3.0 TR
```
