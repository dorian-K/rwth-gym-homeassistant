from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN


async def _async_has_devices(hass: HomeAssistant) -> bool:
    return True


config_entry_flow.register_discovery_flow(
    DOMAIN, "NEW_NAME", _async_has_devices)
