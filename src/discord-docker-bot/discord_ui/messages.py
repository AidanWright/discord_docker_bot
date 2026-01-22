import discord
import docker
from config import BOT
from config import DISCORD_CHANNEL_ID
from config import LOGGER
from discord_ui.views import create_container_view

# Initialize Docker client
client = docker.from_env()

# Store message IDs for each container
container_messages = {}


def get_container_message(container) -> str:
    """Generate the message content for a container."""
    status_emoji = {
        "running": "▶️",
        "exited": "⏹️",
        "restarting": "🔄",
        "paused": "⏸️",
    }.get(container.status, "❓")

    return f"{status_emoji} **{container.name}** - {container.status}"


async def send_discord_message(channel, container):
    """Send a Discord message for a container."""
    message = await channel.send(
        get_container_message(container),
        view=create_container_view(container.name),
    )
    container_messages[container.name] = message.id


async def update_all_container_messages():
    """Update all container status messages."""
    try:
        docker_channel = BOT.get_channel(int(DISCORD_CHANNEL_ID))
        if not docker_channel:
            LOGGER.error("Could not find Discord channel")
            return

        container_list = client.containers.list(all=True)
        container_names = {c.name for c in container_list}

        # Update existing messages
        for container in container_list:
            if container.name in container_messages:
                try:
                    message = await docker_channel.fetch_message(
                        container_messages[container.name]
                    )
                    new_content = get_container_message(container)
                    await message.edit(
                        content=new_content,
                        view=create_container_view(container.name),
                    )
                except discord.NotFound:
                    LOGGER.warning(
                        f"Message for container {container.name} not found, will recreate"  # noqa: E501
                    )
                    del container_messages[container.name]
                    await send_discord_message(docker_channel, container)
                except Exception as e:
                    LOGGER.error(f"Error updating message for {container.name}: {e}")
            else:
                # Send new message if it doesn't exist
                try:
                    await send_discord_message(docker_channel, container)
                except Exception as e:
                    LOGGER.error(f"Error sending message for {container.name}: {e}")

        # Remove messages for deleted containers
        deleted_containers = set(container_messages.keys()) - container_names
        for container_name in deleted_containers:
            try:
                message = await docker_channel.fetch_message(
                    container_messages[container_name]
                )
                await message.delete()
            except discord.NotFound:
                pass
            except Exception as e:
                LOGGER.error(f"Error deleting message for {container_name}: {e}")
            del container_messages[container_name]
    except Exception as e:
        LOGGER.error(f"Error updating container messages: {e}")
