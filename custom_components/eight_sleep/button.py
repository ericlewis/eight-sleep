"""Base soundscape playback command buttons."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import EightSleepBaseEntity, EightSleepConfigEntryData
from .const import DOMAIN
from .pyEight.eight import EightSleep
from .pyEight.user import EightUser


PLAY_DESCRIPTION = ButtonEntityDescription(
    key="base_play_soundscape",
    name="Play Soundscape",
    icon="mdi:play",
)
PAUSE_DESCRIPTION = ButtonEntityDescription(
    key="base_pause_soundscape",
    name="Pause Soundscape",
    icon="mdi:pause",
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Base soundscape command buttons when a Base is present."""
    data: EightSleepConfigEntryData = hass.data[DOMAIN][entry.entry_id]
    eight = data.api
    user = eight.base_user
    if user is None:
        async_add_entities([])
        return

    async_add_entities([
        BaseSoundscapeButton(entry, data.base_coordinator, eight, user, PLAY_DESCRIPTION, user.play_soundscape),
        BaseSoundscapeButton(entry, data.base_coordinator, eight, user, PAUSE_DESCRIPTION, user.pause_soundscape),
    ])


class BaseSoundscapeButton(EightSleepBaseEntity, ButtonEntity):
    """A command-only button for Base soundscape playback."""

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: DataUpdateCoordinator,
        eight: EightSleep,
        user: EightUser,
        description: ButtonEntityDescription,
        command,
    ) -> None:
        super().__init__(entry, coordinator, eight, user, description.key, base_entity=True)
        self.entity_description = description
        self._command = command

    async def async_press(self) -> None:
        """Send the playback command; do not persist or infer player state."""
        await self._generic_service_call(self._command)
