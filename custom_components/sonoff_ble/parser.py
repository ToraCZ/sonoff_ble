from __future__ import annotations

import logging
from typing import Any

import homeassistant.helpers.device_registry as dr
from home_assistant_bluetooth import BluetoothServiceInfoBleak
from homeassistant.components import bluetooth
from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothDataUpdate,
)
from homeassistant.config_entries import SOURCE_BLUETOOTH, ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    ACTION_DOUBLE,
    ACTION_LONG,
    ACTION_SHORT,
    BEEF_ID,
    DEVICE_R5,
    DEVICE_SMATE,
    DOMAIN,
    EVENT_DOMAIN,
    MAC_ADDRESS,
    SWITCH_1,
    SWITCH_2,
    SWITCH_3,
    SWITCH_4,
    SWITCH_5,
    SWITCH_6,
)
from .util import event_type

_LOGGER = logging.getLogger(__name__)


class SonoffBLEParser:
    """Parser for Sonoff BLE device advertisements."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the parser."""
        self.hass = hass
        self.entry = entry

    @callback
    def update(
        self, service_info: BluetoothServiceInfoBleak | PassiveBluetoothDataUpdate
    ) -> None:
        """Process BLE advertisement data."""
        if isinstance(service_info, PassiveBluetoothDataUpdate):
            return

        if service_info.address != MAC_ADDRESS:
            return

        try:
            self._process_advertisement(service_info)
        except Exception as err:
            _LOGGER.exception("Unexpected error processing advertisement: %s", err)

    def _process_advertisement(self, service_info: BluetoothServiceInfoBleak) -> None:
        """Process the BLE advertisement data."""
        uuids = service_info.service_uuids
        _LOGGER.debug(
            "Received %d UUIDs: %s", len(uuids), [uuid.split("-")[0] for uuid in uuids]
        )

        # Validate UUID count
        if len(uuids) < 6:
            _LOGGER.debug("Insufficient UUIDs: %d, expected at least 6", len(uuids))
            return

        # Validate BEEF prefix
        beef_data = "".join([uuid.split("-")[0] for uuid in uuids[0:2]]).upper()
        if beef_data != BEEF_ID:
            _LOGGER.debug("Invalid BEEF prefix: %s, expected: %s", beef_data, BEEF_ID)
            return

        # Process data
        try:
            device_info = self._parse_advertisement_data(uuids)
            if device_info:
                # Get or create device entry
                device = dr.async_get(self.hass).async_get_or_create(
                    config_entry_id=self.entry.entry_id,
                    name=device_info["device_name"],
                    manufacturer="Sonoff",
                    model=device_info["device_type"],
                    identifiers={(DOMAIN, device_info["device_id"])},
                )
                # Fire the event
                self._fire_event(device, device_info)

        except ValueError as err:
            _LOGGER.warning("Failed to parse advertisement data: %s", err)

    def _parse_advertisement_data(self, uuids: list[str]) -> dict[str, Any] | None:
        """Parse the advertisement data and return device info."""
        # Extract and combine data
        last_4_uuids = uuids[-4:]
        cleaned = uuids[0:2] + last_4_uuids
        btdata = "".join([uuid.split("-")[0] for uuid in cleaned]).upper()

        if len(btdata) != 48:
            raise ValueError(
                f"Invalid data length: {len(btdata)}, expected 48 characters"
            )

        # Parse device information
        device_type = self._get_device_type(btdata[22:24])
        device_id = btdata[26:32]

        # Decrypt and parse action data
        encrypted_data = bytes.fromhex(btdata[32:48])
        decrypted = self._decrypt(encrypted_data)

        if len(decrypted) < 2:
            raise ValueError(f"Insufficient decrypted data: {len(decrypted)} bytes")

        action = self._get_action(decrypted[0])
        switch = self._get_switch(decrypted[1])

        return {
            "device_type": device_type,
            "device_id": device_id,
            "action": action,
            "switch": switch,
            "device_name": f"{device_type} {device_id}",
        }

    def _fire_event(self, device: dr.DeviceEntry, device_info: dict[str, Any]) -> None:
        """Fire event for device action."""
        self.hass.bus.async_fire(
            EVENT_DOMAIN,
            {
                "device_id": device.id,
                "type": event_type(device_info["switch"], device_info["action"]),
            },
        )

    @staticmethod
    def _decrypt(input_bytes: bytes) -> bytes:
        """Decrypt the input bytes using XOR."""
        if len(input_bytes) < 2:
            return b""
        return bytes(
            input_bytes[0] ^ input_bytes[i + 1] for i in range(len(input_bytes) - 1)
        )

    @staticmethod
    def _get_switch(code: int) -> str:
        """Map switch code to switch identifier."""
        switch_map = {
            102: SWITCH_1,
            103: SWITCH_2,
            100: SWITCH_3,
            101: SWITCH_4,
            98: SWITCH_5,
            99: SWITCH_6,
        }
        if code not in switch_map:
            raise ValueError(f"Invalid switch code: {code}")
        return switch_map[code]

    @staticmethod
    def _get_action(code: int) -> str:
        """Map action code to action identifier."""
        action_map = {225: ACTION_SHORT, 224: ACTION_DOUBLE, 227: ACTION_LONG}
        if code not in action_map:
            raise ValueError(f"Invalid action code: {code}")
        return action_map[code]

    @staticmethod
    def _get_device_type(code: str) -> str:
        """Map device code to device type."""
        device_map = {"46": DEVICE_SMATE, "47": DEVICE_R5}
        if code not in device_map:
            raise ValueError(f"Invalid device code: {code}")
        return device_map[code]
