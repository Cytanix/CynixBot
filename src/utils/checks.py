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
import json
import os
from typing import TYPE_CHECKING, Callable

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from src.utils.errors import NSFWEndpointCalled

# from utils.redis_io import is_user_blacklisted

if TYPE_CHECKING:
    from typing import Any


load_dotenv()

with open("src/utils/endpoints.json", "r", encoding="utf-8") as f:
    endpoints = json.load(f)

sfw_endpoints = endpoints["SFW_ENDPOINTS"]
nsfw_endpoints = endpoints["NSFW_ENDPOINTS"]


async def nsfw_endpoint(endpoint: str) -> bool:
    """This function checks if the given endpoint is NSFW"""
    if endpoint in nsfw_endpoints:
        raise NSFWEndpointCalled()
    return False


# def app_not_blacklisted() -> Callable[[app_commands.Command], app_commands.Command]:
#    """This function checks if the user is not blacklisted for an app command"""
#    async def predicate(interaction: discord.Interaction) -> bool:
#      return not await is_user_blacklisted(interaction.user.id)
#   return app_commands.check(predicate) # type: ignore

# def prefix_not_blacklisted() -> Callable[[commands.Command], commands.Command]:
#    """This function checks if the user is not blacklisted for a prefix command"""
#    async def predicate(ctx: discord.ext.commands.Context) -> bool:
#        return not await is_user_blacklisted(ctx.author.id)
#    return commands.check(predicate) # type: ignore


owners = list(map(int, json.loads(os.getenv("OWNERS", "[]"))))
devs = list(map(int, json.loads(os.getenv("DEVS", "[]"))))


def is_owner(ctx: commands.Context) -> bool:
    """This function checks if the given user is an owner"""
    return ctx.author.id in owners


def is_dev(ctx: commands.Context) -> bool:
    """This function checks if the given user is a dev"""
    return ctx.author.id in devs


def owner_or_dev(ctx: commands.Context) -> bool:
    """This function checks if the given user is an owner or a dev"""
    return ctx.author.id in owners or ctx.author.id in devs


def owner_or_permissions(**perms: Any) -> bool:
    """This function checks if the given user is an owner or has permissions"""

    async def predicate(inter: discord.Interaction) -> bool:
        """Predicate for the check"""
        if inter.author.id in owners:
            return True
        return await commands.has_permissions(**perms).predicate(inter)

    return app_commands.check(predicate)


def app_is_owner() -> Callable[[Callable], app_commands.Command]:
    """Check if the user is an owner."""

    async def predicate(inter: discord.Interaction) -> bool:
        """Predicate for the check"""
        return inter.user.id in owners

    return app_commands.check(predicate)


def app_is_dev() -> Callable[[Callable], app_commands.Command]:
    """Check if the user is a dev."""

    async def predicate(inter: discord.Interaction) -> bool:
        """Predicate for the check"""
        return inter.user.id in devs

    return app_commands.check(predicate)


def app_is_owner_or_dev() -> Callable[[Callable], app_commands.Command]:
    """Check if the user is an owner OR a dev."""

    async def predicate(inter: discord.Interaction) -> bool:
        """Predicate for the check"""
        return inter.user.id in owners or inter.user.id in devs

    return app_commands.check(predicate)
