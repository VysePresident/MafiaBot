"""
Author: Geo
Date: July 29th, 2023

This module is used strictly for setting up the bot and reloading extensions.
"""

from bot import MafiaBot
from discord.ext import commands
from db import DatabaseManager
from config import Config

bot_token = ''
try:
    from aso_key_file_name import mysterious_key_of_power, username, password, host, database
    bot_token = mysterious_key_of_power
    print("Main key imported")
except ImportError:
    try:
        from test_token import test_token, username, password, host, database
        bot_token = test_token
        print("Test bot key imported")
    except ImportError:
        bot_token = test_token = mysterious_key_of_power = None
        print("All imports failed.  Using blank key")

bot = MafiaBot(command_prefix="%", token=bot_token)

@bot.event
async def on_ready():

    await bot.load_extension("admin_commands")
    await bot.load_extension("player_commands")

    await db_conn()

    Config.dbManager = DatabaseManager(Config.username, Config.password, Config.db_host, Config.database, bot)
    print(f'This is username: {Config.username} this is password: {Config.password}')
    print(f'This is host: {Config.db_host} this is database: {Config.database}')

    await Config.dbManager.connect()
    connResult = await Config.dbManager.setConfigurations()
    print(f"THIS IS connResult: {connResult}")

    if bot.get_channel(1110103139065012244):
        channel = bot.get_channel(1110103139065012244)
        await channel.send('Bot is online!')

    Config.bot = bot  # WIP - Laziest solution to connect player.kill() to votecount().  Figure out later.
    print("Bot is online")


@bot.command()
@commands.has_permissions(administrator=True)
async def reloadext(ctx):
    """Reload extensions on the bot"""
    print("Reloading extensions!")
    await bot.reload_extension("admin_commands")
    await bot.reload_extension("player_commands")


async def db_conn():
    try:
        from aso_key_file_name import username, password, host, database
        print("Main db info imported")
        Config.username = username
        Config.password = password
        Config.db_host = host
        Config.database = database
    except ImportError:
        try:
            from test_token import username, password, host, database
            print("Test db info imported")
            Config.username = username
            Config.password = password
            Config.db_host = host
            Config.database = database
        except ImportError:
            username = password = host = database = None
            print("All imports failed. Not connected to database")
    

bot.run(bot_token)
