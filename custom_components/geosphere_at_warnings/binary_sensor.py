"""Binary Sensor for MeteoAlarm.eu."""

from __future__ import annotations

import datetime
import logging
from datetime import timedelta
from typing import TYPE_CHECKING

import homeassistant.const
import voluptuous
from geosphere_at_warnings import geosphere
from homeassistant.components.binary_sensor import (
    PLATFORM_SCHEMA as BINARY_SENSOR_PLATFORM_SCHEMA,
)
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers import config_validation

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

logger = logging.getLogger(__name__)

ATTRIBUTION = "Data by Geosphere Austria"

CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_ADVANCED_WARNING_TIME = "advanced_warning_time"

DEFAULT_NAME = "geosphere-at"

SCAN_INTERVAL = timedelta(minutes=5)

PLATFORM_SCHEMA = BINARY_SENSOR_PLATFORM_SCHEMA.extend(
    {
        voluptuous.Required(CONF_LATITUDE): config_validation.latitude,
        voluptuous.Required(CONF_LONGITUDE): config_validation.longitude,
        voluptuous.Required(CONF_ADVANCED_WARNING_TIME): config_validation.timedelta,
    },
)


def setup_platform(
    hass: HomeAssistant,  # noqa: ARG001
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,  # noqa: ARG001
) -> None:
    latitude = config[CONF_LATITUDE]
    longitude = config[CONF_LONGITUDE]
    name = config[homeassistant.const.CONF_NAME]
    advanced_warning_time = config[CONF_ADVANCED_WARNING_TIME]

    add_entities(
        new_entities=[GeosphereAtBinarySensor(name=name, latitude=latitude, longitude=longitude, advanced_warning_time=advanced_warning_time)],
        update_before_add=True,
    )


class GeosphereAtBinarySensor(BinarySensorEntity):
    _attr_attribution = ATTRIBUTION
    _attr_device_class = BinarySensorDeviceClass.SAFETY

    def __init__(self, name: str, latitude: float, longitude: float, advanced_warning_time: datetime.timedelta) -> None:
        self._attr_name = name
        self.location = geosphere.Location(latitude=latitude, longitude=longitude)
        self.advanced_warning_time = advanced_warning_time

    def update(self) -> None:
        self._attr_extra_state_attributes = {}
        self._attr_is_on = False

        try:
            all_warnings = geosphere.get_relevant_warnings(self.location)
        except Exception:
            logger.exception("Error fetching warnings")
            return

        relevant_warnings = all_warnings.get_relevant(advanced_warning_time=timedelta(hours=0))
        if len(relevant_warnings) == 0:
            return

        relevant_warnings_sorted = sorted(relevant_warnings, key=lambda w: w.level, reverse=True)
        highest_warning = relevant_warnings_sorted[0]

        self._attr_is_on = True
        self._attr_extra_state_attributes = {
            "eventType": highest_warning.type.name,
            "eventLevel": highest_warning.level.name,
        }
