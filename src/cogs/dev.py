##  © 2025 SpiritTheWalf/Cytanix. All rights reserved.
#
#  This file is part of the CynixBot project.
#  The source code of this component is proprietary and confidential.
#
#  Unauthorized copying, modification, distribution, or use
#  of this file, in whole or in part, is strictly prohibited.
#
#  Written by Spirit Pearce, 2025.
#

import asyncio
import os
import sys

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from src.utils.checks import app_is_owner_or_dev

load_dotenv()

portainer_key = {"X-API-KEY": os.getenv("PORTAINER_API_KEY")}


@app_commands.allowed_contexts(guilds=True, dms=True)
class Dev(commands.GroupCog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="pull", description="Pull the latest code changes from Git")
    @app_commands.describe(restart="Restart the bot?")
    async def pull(self, inter: discord.Interaction, restart: bool) -> None:
        await inter.response.defer(thinking=True)
        await inter.followup.send("Pulling changes...")

        process = await asyncio.create_subprocess_exec(
            "git", "pull", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode().strip() or stderr.decode().strip()

        if "Already up to date" in output:
            await inter.followup.send("No updates found.")
            return

        await inter.followup.send("Changes pulled.")

        if restart:
            await inter.followup.send("Restarting...")
            os.execv(sys.executable, [sys.executable] + sys.argv)

        await inter.followup.send("Restart not requested.")

    @app_is_owner_or_dev()
    @app_commands.command(name="restart", description="Restart the bot.")
    async def restart(self, inter: discord.Interaction) -> None:
        await inter.response.send_message("Restarting...", ephemeral=True)
        os.execv(sys.executable, [sys.executable] + sys.argv)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dev(bot))
