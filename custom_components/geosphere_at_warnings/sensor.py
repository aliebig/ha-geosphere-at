"""Sensor platform for Cookiecutter Home Assistant Custom Component Instance."""

from collections.abc import Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from. import geosphere, const, entity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_devices: Callable) -> None:
    coordinator = hass.data[const.DOMAIN][entry.entry_id]
    async_add_devices([GeosphereAtWarningsSensor(coordinator, entry)])


class GeosphereAtWarningsSensor(entity.GeosphereAtWarningsEntity):
    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{const.DEFAULT_NAME}_{const.SENSOR}"

    @property
    def state(self) -> str:
        warnings: geosphere.GeosphereWarnings | None = self.coordinator.data.get("warnings")

        if warnings:
            result = warnings.get_relevant(advanced_warning_time=self.config_entry.data["advanced_warning_time"])
            if result:
                return f"Warnings: {len(result)}"

        return "No Warnings"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return const.ICON

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "geosphere_at_warnings__sensor__device_class"
