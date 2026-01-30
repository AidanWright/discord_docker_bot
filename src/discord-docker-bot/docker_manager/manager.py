import discord
import docker
from config import BOT
from config import LOGGER
from discord_ui.messages import update_all_container_messages
import utils.formatting

# Initialize Docker client
client = docker.from_env()


async def handle_container_action(
    interaction: discord.Interaction, action: str, container_name: str
):
    """Handle start, stop, and restart actions for a container."""
    try:
        await interaction.response.defer()
        container = client.containers.get(container_name)

        if not await BOT.is_owner(interaction.user):
            await interaction.followup.send(
                "❌ You do not have permission to use this button.",
                ephemeral=True,
            )
            return

        if action == "start":
            container.start()
            response = f"✅ Container **{container_name}** has been started."
        elif action == "stop":
            container.stop(timeout=10)
            response = f"✅ Container **{container_name}** has been stopped."
        elif action == "restart":
            container.restart()
            response = f"✅ Container **{container_name}** has been restarted."
        elif action == "logs":
            logs = container.logs(tail=100).decode("utf-8")
            formatted_logs = utils.formatting.remove_ansi_codes(logs)
            if len(formatted_logs) > 1900:
                formatted_logs = formatted_logs[-1900:]  # Truncate to last 1900 characters
            response = f"ℹ️ Container **{container_name}** logs:\n```{formatted_logs}```"
        await interaction.followup.send(response, ephemeral=True)
        LOGGER.info(f"Container {container_name} {action}ed successfully")

        # Update the message after the action
        await update_all_container_messages()

    except docker.errors.NotFound:
        await interaction.followup.send(
            f"❌ Container **{container_name}** not found.", ephemeral=True
        )
        LOGGER.error(f"Container {container_name} not found")
    except docker.errors.APIError as e:
        await interaction.followup.send(
            f"❌ Error performing {action} on **{container_name}**: {str(e)}",
            ephemeral=True,
        )
        LOGGER.error(f"Error performing {action} on {container_name}: {str(e)}")
    except Exception as e:
        await interaction.followup.send(
            f"❌ Unexpected error: {str(e)}", ephemeral=True
        )
        LOGGER.error(f"Unexpected error: {str(e)}")
