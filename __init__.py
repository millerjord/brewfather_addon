import requests
import json
import base64
import asyncio
import logging
from datetime import datetime

from homeassistant.const import (CONF_PASSWORD, CONF_USERNAME)

from homeassistant import config_entries, core

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ("sensor")

async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up platforms from a ConfigEntry."""
    url = entry.data["url"]
    hass.data[DOMAIN][entry.entry_id] = SensorManager(hass, url)

    if not entry.unique_id:
        hass.config_entries.async_update_entry(entry, unique_id="brewfather")

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True
