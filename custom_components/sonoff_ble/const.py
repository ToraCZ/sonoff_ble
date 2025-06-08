"""Constants for the Sonoff BLE integration."""
from __future__ import annotations

from typing import Final

DOMAIN: Final = "sonoff_ble"
EVENT_DOMAIN: Final = f"{DOMAIN}_event"
MAC_ADDRESS: Final = "66:55:44:33:22:11"
ENTRY_ID: Final = "sonoff_ble_single_entry"
BEEF_ID: Final = "1BEEFFFF4AF678C8"

# Switch identifiers
SWITCH_1: Final = "s1"
SWITCH_2: Final = "s2"
SWITCH_3: Final = "s3"
SWITCH_4: Final = "s4"
SWITCH_5: Final = "s5"
SWITCH_6: Final = "s6"
SWITCHES: Final = [SWITCH_1, SWITCH_2, SWITCH_3, SWITCH_4, SWITCH_5, SWITCH_6]

# Device types
DEVICE_SMATE: Final = "S-Mate"
DEVICE_R5: Final = "SwitchMan R5"

# Action types
ACTION_SHORT: Final = "short"
ACTION_DOUBLE: Final = "double"
ACTION_LONG: Final = "long"
ACTIONS: Final = [ACTION_SHORT, ACTION_DOUBLE, ACTION_LONG]

# Configuration
CONF_COORDINATOR: Final = "coordinator"
DEFAULT_SCAN_INTERVAL: Final = 60
MIN_SCAN_INTERVAL: Final = 10
