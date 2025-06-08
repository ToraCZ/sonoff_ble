from __future__ import annotations

import logging
from typing import Any

import homeassistant.helpers.device_registry as dr
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components import bluetooth
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import DOMAIN, ENTRY_ID, MAC_ADDRESS
from .parser import SonoffBLEParser

_LOGGER = logging.getLogger(__name__)


class SonoffBLEConfigurationFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sonoff BLE."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the user step."""
        # Set unique ID and abort if already configured
        await self.async_set_unique_id(ENTRY_ID)
        self._abort_if_unique_id_configured()

        # Create the entry since it's not already configured
        return self.async_create_entry(
            title="Sonoff BLE",
            data={
                "discovered_via_bluetooth": True,
                "discovery_address": MAC_ADDRESS,
            },
        )
