from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import const, coordinator


class GeosphereAtWarningsEntity(CoordinatorEntity):
    def __init__(self, coordinator_: coordinator.GeosphereAtWarningsDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator_)
        self.config_entry = config_entry

    @property
    def unique_id(self) -> str:
        return self.config_entry.entry_id

    @property
    def device_info(self) -> dict:
        return {
            "identifiers": {(const.DOMAIN, self.unique_id)},
            "name": const.NAME,
            "model": const.VERSION,
            "manufacturer": const.NAME,
        }

    @property
    def device_state_attributes(self) -> dict:
        """Return the state attributes."""
        return {
            "attribution": const.ATTRIBUTION,
            "id": str(self.coordinator.data.get("id")),
            "integration": const.DOMAIN,
        }
