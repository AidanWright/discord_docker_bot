import discord
import docker_manager.manager
from config import BOT
from config import DISCORD_CHANNEL_ID
from config import DISCORD_TOKEN
from config import LOGGER
from discord.ext import tasks
from discord_ui.messages import update_all_container_messages


@tasks.loop(minutes=5)
async def update_container_statuses():
    """Background task to update container statuses every 5 minutes"""
    LOGGER.info("Updating container statuses")
    await update_all_container_messages()


@update_container_statuses.before_loop
async def before_update():
    """Wait for bot to be ready before starting the loop"""
    await BOT.wait_until_ready()


# on_ready event can trigger multiple times, so we should be careful to only
# "initialize" our application once.
@BOT.event
async def on_ready():
    LOGGER.info(f"Bot {BOT.user} is connected and ready!")

    # Start the background update task only once
    if not update_container_statuses.is_running():
        # Only initialize messages on first startup
        docker_channel = BOT.get_channel(int(DISCORD_CHANNEL_ID))

        # Delete all previous messages from the channel
        async for message in docker_channel.history(limit=30):
            await message.delete()

        update_container_statuses.start()


@BOT.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return

    custom_id = interaction.data.get("custom_id", "")

    # Parse the custom_id to get action and container name
    if "_" not in custom_id:
        return

    action, container_name = custom_id.split("_", 1)

    if action not in ["start", "stop", "restart"]:
        return

    await docker_manager.manager.handle_container_action(
        interaction, action, container_name
    )


# Obtiene el token desde las variables de entorno
if DISCORD_TOKEN:
    BOT.run(DISCORD_TOKEN)
else:
    LOGGER.error("Discord token is undefined at environment vars.")
