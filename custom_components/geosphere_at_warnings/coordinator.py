import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from . import const, geosphere

logger = logging.getLogger(__name__)


class GeosphereAtWarningsDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass: HomeAssistant,
        client: geosphere.Client,
    ) -> None:
        """Initialize."""
        self.api = client
        self.platforms = []

        super().__init__(hass, logger, name=const.DOMAIN, update_interval=const.QUERY_INTERVAL)

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.api.async_get_data()
        except Exception as exception:
            raise UpdateFailed from exception
