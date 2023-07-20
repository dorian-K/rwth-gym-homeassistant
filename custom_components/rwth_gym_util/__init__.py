"""The FitX Utilization integration."""
from __future__ import annotations
import logging

from aionanoleaf import ClientConnectionError
from .rwth_gym import get_auslastung_number

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DATA_COORDINATOR, DEFAULT_UPDATE_INTERVAL, DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]
_LOGGER = logging.getLogger(__name__)
# _LOGGER.setLevel("DEBUG")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up FitX Utilization from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    coordinator = RWTHDataUpdateCoordinator(hass, entry=entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        DATA_COORDINATOR: coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class RWTHDataUpdateCoordinator(DataUpdateCoordinator):
    """RWTH Data Update Coordinator"""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        self.hass = hass

        self.entry = entry
        self.disable_session = False

        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=DEFAULT_UPDATE_INTERVAL
        )

    async def _async_update_data(self) -> dict:
        try:
            util = await get_auslastung_number()
        except ClientConnectionError as error:
            raise UpdateFailed(error) from error
        return {"utilization": util}
