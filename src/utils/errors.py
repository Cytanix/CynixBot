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
from typing import Union

from aiohttp.web_exceptions import HTTPUnauthorized
from discord.app_commands import CheckFailure


class NotOwner(CheckFailure):
    """Check if the user is an owner OR a dev."""

    def __init__(self, user_id: int, message: Union[str, None] = None):
        self.user_id = user_id
        super().__init__(message or "You are not an owner of this bot!")


class InvalidEndpointError(ValueError):
    """Error that is raised when an invalid endpoint is requested from the API"""

    def __init__(self, endpoint: str) -> None:
        super().__init__(f"Invalid endpoint {endpoint}")


class NSFWEndpointCalled(Exception):
    """Error that is raised when an NSFW endpoint is requested from the API"""

    def __init__(self) -> None:
        super().__init__(
            "NSFW endpoints have been disabled for this guild. "
            "If you feel this is a mistake, please contact SpiritTheWalf"
        )


class UnauthorizedError(HTTPUnauthorized):
    """Error that is raised when an unauthorized request is made to the API"""

    def __init__(self) -> None:
        super().__init__(reason="Unauthorized, please make sure your API key is correct.")
