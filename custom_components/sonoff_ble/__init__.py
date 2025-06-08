from __future__ import annotations

import logging

from homeassistant.components.bluetooth import BluetoothScanningMode
from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothProcessorCoordinator,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_COORDINATOR, DOMAIN, MAC_ADDRESS
from .parser import SonoffBLEParser

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    parser = SonoffBLEParser(hass, entry)
    coordinator = hass.data.setdefault(DOMAIN, {})[CONF_COORDINATOR] = (
        PassiveBluetoothProcessorCoordinator(
            hass,
            _LOGGER,
            address=MAC_ADDRESS,
            mode=BluetoothScanningMode.PASSIVE,
            update_method=parser.update,
        )
    )
    # only start after all platforms have had a chance to subscribe
    entry.async_on_unload(coordinator.async_start())
    return True
