import discord
from config import BOT
from config import LOGGER
from discord.ext import commands


@BOT.command()
@commands.is_owner()
async def sync(ctx):
    """Synchronize slash commands with Discord."""
    try:
        guilds = [guild.id for guild in ctx.bot.guilds]
        LOGGER.debug(f"The {ctx.bot.user.name} bot is in {len(guilds)} Guilds.\
            The guilds IDs list: {guilds}")
        for guildId in guilds:
            guild = discord.Object(id=guildId)
            print(f"Deleting commands from {guildId}.....")
            ctx.bot.tree.clear_commands(guild=guild, type=None)
            await ctx.bot.tree.sync(guild=guild)
            print(f"Deleted commands from {guildId}!")
            continue
        LOGGER.debug("Deleting global commands.....")
        ctx.bot.tree.clear_commands(guild=None, type=None)
        await ctx.bot.tree.sync(guild=None)
        LOGGER.debug("Deleted global commands!")
        synced = await ctx.bot.tree.sync()
        LOGGER.debug(f"Synchronized slash commands: {len(synced)} commands")
        await ctx.send("Command tree synced.")
    except Exception as e:
        LOGGER.error(f"Error when synchronizing slash commands: {e}")
