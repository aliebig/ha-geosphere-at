"""Config flow for Emu M-Bus Center."""

from __future__ import annotations

import logging

import homeassistant.helpers.selector as input_selector
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult

from . import const

logger = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=const.DOMAIN):
    async def async_step_user(self, user_input: dict | None = None) -> ConfigFlowResult:
        errors = {}
        if user_input is not None:
            location = user_input.get("location", {})
            if location:
                return self.async_create_entry(
                    title=user_input.get("name", "Geosphere AT Warnings"),
                    data={
                        "latitude": location.get("latitude"),
                        "longitude": location.get("latitude"),
                        "name": user_input.get("name", "Geosphere AT Warnings"),
                    },
                )
            logger.error("user input missing location")
            errors["invalid_location"] = "invalid_location"
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("name"): str,
                    vol.Required("location"): input_selector.LocationSelector(),
                },
            ),
            errors=errors,
        )
