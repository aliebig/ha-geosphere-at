"""The Emu M-Bus Center integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from . import const, geosphere

logger = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    hass.data.setdefault(const.DOMAIN, {})

    client_config = geosphere.ClientConfig(
        location=geosphere.Location(latitude=config_entry.data["latitude"], longitude=config_entry.data["longitude"]),
        advanced_warning_time=config_entry.data["advanced_warning_time"],
    )
    client = geosphere.Client(client_config, async_get_clientsession(hass))

    hass.data[const.DOMAIN][config_entry.entry_id] = client

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[const.DOMAIN].pop(entry.entry_id)

    return unload_ok
