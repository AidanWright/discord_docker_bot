import logging
import os

import discord
from discord.ext import commands

# "An intent basically allows a bot to subscribe to specific buckets of events."
# Some intents, like message content, are privileged and need to be enabled
# both here *and* in the Discord Developer Portal.
intents = discord.Intents.default()
intents.message_content = True

# If no prefix is set, returns NONE, which essentially disables prefix commands.
BOT_PREFIX = os.getenv("BOT_PREFIX")
BOT = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# Environment variables
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Logging configuration
log_level = logging.getLevelNamesMapping().get(
    os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO
)
discord.utils.setup_logging(level=log_level, root=True)
LOGGER = logging.getLogger("discord-docker-bot")
