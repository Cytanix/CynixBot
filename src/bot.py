#  © 2025 SpiritTheWalf/Cytanix. All rights reserved.
#
#  This file is part of the CynixBot project.
#  The source code of this component is proprietary and confidential.
#
#  Unauthorized copying, modification, distribution, or use
#  of this file, in whole or in part, is strictly prohibited.
#
#  Written by Spirit Pearce, 2025.
#
import os
import sys
import traceback
from pathlib import Path
from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from discord.ext.commands import ExtensionError
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
sys.path.append(str(Path(__file__).parent))

if TYPE_CHECKING:
    from typing import Any


async def cog_loader(bot_inst: commands.Bot) -> None:
    """Loads all cogs plus jsk"""
    await bot_inst.load_extension("jishaku")
    for file in os.listdir(os.path.join(os.path.dirname(__file__), "cogs")):
        if file.endswith(".py") and file != "__init__.py":
            try:
                await bot_inst.load_extension(f"cogs.{file[:-3]}")
                print(f"Successfully loaded cog {file[:-3]}")
            except ExtensionError as e:
                print(f"Failed to load cog {file[:-3]}: {e}")
                print(traceback.format_exc())


class CynixBot(commands.Bot):
    """The main bot class."""

    def __init__(self, environment: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.environment = environment if environment else "DEVELOPMENT"
        self.version = "0.0.1"
        self.session_cmd_cnt = 0

    async def setup_hook(self) -> None:
        """Called when the bot starts."""
        await cog_loader(self)

    async def on_ready(self) -> None:
        """Called when the bot is ready."""
        print(f"Logged in as {self.user} (ID: {self.user.id}) | {self.environment} | {self.version}")


if __name__ == "__main__":
    env = os.getenv("BOT_ENV") or "DEVELOPMENT"
    env = env.upper().strip()

    # Prefix selection
    prefix = "C! " if env == "PRODUCTION" else "CD! "

    # Token selection
    token = os.getenv("DISCORD_TOKEN") if env == "PRODUCTION" else os.getenv("DEV_TOKEN")

    bot = CynixBot(environment=env, command_prefix=commands.when_mentioned_or(prefix), intents=intents)

    bot.run(token)
