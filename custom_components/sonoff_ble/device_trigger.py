from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from homeassistant.components.homeassistant.triggers import event as event_trigger
from homeassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE
from homeassistant.core import HomeAssistant
import homeassistant.helpers.device_registry as dr

from .const import (
    DOMAIN,
    EVENT_DOMAIN,
    SWITCHES,
    ACTIONS,
    SWITCH_1,
    SWITCH_2,
    SWITCH_3,
    ACTION_SHORT,
    DEVICE_R5,
    DEVICE_SMATE,
)
from .util import event_type


ALL_TRIGGERS = [event_type(switch, action) for switch in SWITCHES for action in ACTIONS]

TRIGGERS = {
    # R5 supports all 6 switches and all 3 actions
    DEVICE_R5: ALL_TRIGGERS,
    # S-Mate supports 3 switches and short press action only
    DEVICE_SMATE: [
        event_type(switch, ACTION_SHORT) for switch in [SWITCH_1, SWITCH_2, SWITCH_3]
    ],
}

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {vol.Required(CONF_TYPE): vol.In(ALL_TRIGGERS)}
)


async def async_get_triggers(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, Any]]:
    device = dr.async_get(hass).async_get(device_id)
    # Use identifiers or model to determine type
    if not device or not device.model:
        return []
    return [
        {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: DOMAIN,
            CONF_DEVICE_ID: device_id,
            CONF_TYPE: t,
        }
        for t in TRIGGERS.get(device.model, [])
    ]


async def async_attach_trigger(hass, config, action, trigger_info):
    """Attach a trigger."""
    event_config = event_trigger.TRIGGER_SCHEMA(
        {
            event_trigger.CONF_PLATFORM: "event",
            event_trigger.CONF_EVENT_TYPE: EVENT_DOMAIN,
            event_trigger.CONF_EVENT_DATA: {
                CONF_DEVICE_ID: config[CONF_DEVICE_ID],
                CONF_TYPE: config[CONF_TYPE],
            },
        }
    )
    return await event_trigger.async_attach_trigger(
        hass, event_config, action, trigger_info, platform_type="device"
    )
