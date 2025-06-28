import datetime

NAME = "GeoSphere AT Warnings"
DOMAIN = "geosphere_at_warnings"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.1.0"

QUERY_INTERVAL = datetime.timedelta(seconds=10)

ATTRIBUTION = "Data by Geosphere Austria"
ISSUE_URL = "https://github.com/aliebig/ha-geosphere-at/issues"
ICON = "mdi:weather-lightning"

SENSOR = "sensor"
PLATFORMS = [SENSOR]

CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_ADVANCED_WARNING_TIME_MINUTES = "advanced_warning_time_minutes"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
