import datetime
from dataclasses import dataclass
from enum import IntEnum

import requests

BASE_URL = "https://warnungen.zamg.at/wsapp/api"


class WarningLevel(IntEnum):
    YELLOW = 1  # Gelb - Minor weather event
    ORANGE = 2  # Orange - Moderate weather event
    RED = 3  # Rot - Severe weather event
    VIOLET = 4  # Violett - Extreme weather event


class WarningType(IntEnum):
    STORM = 1  # Wind warnings
    RAIN = 2  # Rain warnings
    SNOW = 3  # Snow warnings
    BLACK_ICE = 4  # Ice/Glaze warnings
    THUNDERSTORM = 5  # Thunderstorm/Gewitter warnings
    HEAT = 6  # Heat warnings
    COLD = 7  # Cold warnings


@dataclass
class Location:
    latitude: float
    longitude: float


@dataclass
class GeosphereWarning:
    type: WarningType
    level: WarningLevel
    begin: datetime.datetime
    end: datetime.datetime
    text: str | None = None
    effects: str | None = None
    recommendations: str | None = None

    def is_relevant(self, advanced_warning_time: datetime.timedelta) -> bool:
        now_ = datetime.datetime.now(tz=datetime.UTC)

        if self.end < now_:
            return False
        return not self.begin > now_ + advanced_warning_time

    def is_current(self, advanced_warning_time: datetime.timedelta) -> bool:
        now_ = datetime.datetime.now(tz=datetime.UTC)

        if self.end < now_:
            return False
        return not self.begin > now_ + advanced_warning_time


@dataclass
class GeosphereWarnings:
    warnings: list[GeosphereWarning]

    def get_relevant(self, advanced_warning_time: datetime.timedelta) -> list[GeosphereWarning]:
        return [x for x in self.warnings if x.is_relevant(advanced_warning_time=advanced_warning_time)]

    def has_warnings(self) -> bool:
        return len(self.warnings) > 0


def _parse_warning(data: dict) -> GeosphereWarning:
    properties = data["properties"]
    return GeosphereWarning(
        type=WarningType(properties["rawinfo"]["wtype"]),
        level=WarningLevel(properties["rawinfo"]["wlevel"]),
        begin=datetime.datetime.fromtimestamp(int(properties["rawinfo"]["start"]), tz=datetime.UTC),
        end=datetime.datetime.fromtimestamp(int(properties["rawinfo"]["end"]), tz=datetime.UTC),
        text=properties.get("text"),
        effects=properties.get("auswirkungen"),
        recommendations=properties.get("empfehlungen"),
    )


def _parse_data(data: dict) -> list[GeosphereWarning]:
    warning_data = data.get("properties", {}).get("warnings", [])

    return [_parse_warning(x) for x in warning_data]


def get_relevant_warnings(location: Location) -> GeosphereWarnings:
    data = _fetch_data(location)
    warnings = _parse_data(data)

    return GeosphereWarnings(warnings=warnings)


def _fetch_data(location: Location) -> dict:
    response = requests.get(
        f"{BASE_URL}/getWarningsForCoords?lat={location.latitude}&lon={location.longitude}&lang=de",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()
