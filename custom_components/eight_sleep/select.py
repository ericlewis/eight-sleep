from typing import Callable
from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import EightSleepBaseEntity, EightSleepConfigEntryData
from .const import DOMAIN
from .pyEight.eight import EightSleep
from .pyEight.user import EightUser

PRESETS = ["sleep", "relaxing", "reading"]
MITIGATION_LEVELS = ["low", "medium", "high"]

BASE_PRESET_DESCRIPTION = SelectEntityDescription(
    key="base_preset",
    name="Base Preset",
    icon="mdi:train-car-flatbed",
    options=PRESETS,
)
SNORING_LEVEL_DESCRIPTION = SelectEntityDescription(
    key="snoring_mitigation_level", name="Snoring Mitigation Level", icon="mdi:snore",
    options=MITIGATION_LEVELS,
)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    config_entry_data: EightSleepConfigEntryData = hass.data[DOMAIN][entry.entry_id]
    eight = config_entry_data.api
    coordinator = config_entry_data.base_coordinator

    entities: list[SelectEntity] = []

    user = eight.base_user
    if user:
        async def set_preset(value):
            await user.set_base_preset(value)

        entities.append(EightSelectEntity(
            entry,
            coordinator,
            eight,
            user,
            BASE_PRESET_DESCRIPTION,
            lambda: user.base_preset,
            set_preset))
        async def set_level(value: str):
            current = user.snoring_mitigation
            if current is None:
                return
            await user.set_snoring_mitigation(bool(current["enabled"]), value)

        entities.append(EightSelectEntity(
            entry, coordinator, eight, user, SNORING_LEVEL_DESCRIPTION,
            lambda: (user.snoring_mitigation or {}).get("mitigationLevel"),
            set_level, options=MITIGATION_LEVELS, name="Snoring Mitigation Level",
        ))

    async_add_entities(entities)

class EightSelectEntity(EightSleepBaseEntity, SelectEntity):

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: DataUpdateCoordinator,
        eight: EightSleep,
        user: EightUser,
        entity_description: SelectEntityDescription,
        value_getter: Callable[[], str | None],
        set_value_callback: Callable[[str], None],
        options: list[str] | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(entry, coordinator, eight, user, entity_description.key, base_entity=True)
        self.entity_description = entity_description
        self._attr_options = options or PRESETS
        self._attr_name = name or "Bed Preset"
        self._value_getter = value_getter
        self._set_value_callback = set_value_callback

    @property
    def current_option(self) -> str | None:
        return self._value_getter()

    @property
    def available(self) -> bool:
        if self.entity_description.key == "snoring_mitigation_level":
            return self._user_obj is not None and self._user_obj.snoring_mitigation is not None
        return super().available

    async def async_select_option(self, option: str) -> None:
        result = self._set_value_callback(option)
        if result is not None:
            await result
        await self.coordinator.async_request_refresh()
