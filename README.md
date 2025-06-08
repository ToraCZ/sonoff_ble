# Sonoff BLE - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/toracz/sonoff_ble.svg)](https://github.com/toracz/sonoff_ble/releases)
[![GitHub license](https://img.shields.io/github/license/toracz/sonoff_ble.svg)](https://github.com/toracz/sonoff_ble/blob/main/LICENSE)

A Home Assistant custom integration for using Sonoff BLE devices without the need for gateways.

## Features

- Use Sonoff BLE-enabled devices directly in Home Assistant
- No need to pair with the eWeLink app
- No need for gateways (e.g. MINIR3)
- Local control via Bluetooth - no cloud dependency

## Supported Devices

- Sonoff Switch Mate (S-MATE)
- Sonoff SwitchMan Scene Controller (R5)
- Possibly other Sonoff BLE-enabled devices, not tested yet

## Requirements

- Home Assistant 2025.5.3 or newer
- Bluetooth adapter (and integration) configured on your Home Assistant

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/yourusername/sonoff_ble` as repository
6. Select "Integration" as category
7. Click "Add"
8. Find "Sonoff BLE" in the integrations list and install it
9. Restart Home Assistant

### Manual Installation

1. Download the latest release from [GitHub releases](https://github.com/yourusername/sonoff_ble/releases)
2. Extract the files
3. Copy the `sonoff_ble` folder to your `custom_components` directory
4. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Sonoff BLE"
4. Add the integration
5. Click any button on device you want to add
6. Device should be auto added and visible under **Settings** → **Devices & Services** → **Sonoff BLE**

## Usage

Once a device is discovered and added, you can create automations using the device as a trigger. 

Each device provides the following triggers:

| Trigger Type | Description |
|--------------|-------------|
| Switch N Short Press | Single quick press of switch button |
| Switch N Double Press | Two quick presses of switch button |
| Switch N Long Press | Hold button for 2+ seconds |

The **S-MATE** Has three "buttons" (marked on the device as S1-S3).

The **R5** Has six buttons and supports all three trigger types. Buttons are in the following pattern:

```
  ┌─────────────────────┐
  │                     │
  │  [1]    [2]    [3]  │
  │                     │
  │                     │
  │                     │
  │  [3]    [5]    [6]  │
  │                    S│ <- Logo
  └─────────────────────┘
```

## Known Issues

When sending a lot of events in a short time, some of the events might be discarded. This is caused by BlueZ UUID caching on all Linux devices.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to everyone at the Tasmota forums for [reverse engineering the eWeLink protocols](https://github.com/arendst/Tasmota/discussions/15220)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

**⭐ If you find this integration useful, please consider giving it a star on GitHub!**