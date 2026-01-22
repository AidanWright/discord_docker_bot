import discord


def create_container_view(container_name):
    """Create a new view with buttons for a container."""
    view = discord.ui.View(timeout=None)
    view.add_item(
        discord.ui.Button(
            label="Start",
            style=discord.ButtonStyle.green,
            custom_id=f"start_{container_name}",
        )
    )
    view.add_item(
        discord.ui.Button(
            label="Stop",
            style=discord.ButtonStyle.red,
            custom_id=f"stop_{container_name}",
        )
    )
    view.add_item(
        discord.ui.Button(
            label="Restart",
            style=discord.ButtonStyle.blurple,
            custom_id=f"restart_{container_name}",
        )
    )
    return view
