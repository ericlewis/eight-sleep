"""Public setup tests for Eight Sleep entities without Home Assistant installed."""

from __future__ import annotations

from collections import Counter
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch


def _install_module(name: str, **attributes: object) -> ModuleType:
    """Install a lightweight module stub used at the integration boundary."""
    module = ModuleType(name)
    module.__dict__.update(attributes)
    sys.modules[name] = module
    return module


class _Schema:
    def __init__(self, value: object, **_kwargs: object) -> None:
        self.value = value


class _Platform:
    BUTTON = "button"
    BINARY_SENSOR = "binary_sensor"
    CLIMATE = "climate"
    NUMBER = "number"
    SELECT = "select"
    SENSOR = "sensor"
    SWITCH = "switch"


class _ConfigEntry:
    def __init__(self, entry_id: str, data: dict[str, str]) -> None:
        self.entry_id = entry_id
        self.data = data


class _DeviceInfo(dict):
    def __init__(self, **values: object) -> None:
        super().__init__(values)


class _CoordinatorEntity:
    @classmethod
    def __class_getitem__(cls, _item: object) -> type[_CoordinatorEntity]:
        return cls

    def __init__(self, coordinator: object) -> None:
        self.coordinator = coordinator


class _DataUpdateCoordinator:
    def __init__(
        self,
        *_args: object,
        name: str | None = None,
        update_method: object | None = None,
        **_kwargs: object,
    ) -> None:
        self.name = name
        self.update_method = update_method
        self.refresh_count = 0

    async def async_config_entry_first_refresh(self) -> None:
        self.refresh_count += 1
        if self.update_method is not None:
            await self.update_method()


class _NumberDeviceClass:
    DURATION = "duration"
    FREQUENCY = "frequency"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    TEMPERATURE = "temperature"


class _NumberMode:
    BOX = "box"
    SLIDER = "slider"


class _BinarySensorDeviceClass:
    CONNECTIVITY = "connectivity"
    MAINTENANCE = "maintenance"
    OCCUPANCY = "occupancy"
    PROBLEM = "problem"
    SOUND = "sound"
    UPDATE = "update"


class _SensorDeviceClass:
    DURATION = "duration"
    TEMPERATURE = "temperature"
    TIMESTAMP = "timestamp"


class _SensorStateClass:
    MEASUREMENT = "measurement"


class _UnitOfTemperature:
    CELSIUS = "C"


class _UnitOfTime:
    SECONDS = "s"


class _RequestError(Exception):
    """API request failure stub."""


class _EightSleep:
    """Import-only API type stub; tests inject concrete fake instances."""


class _EightUser:
    """Import-only user type stub."""


async def _no_op_async(*_args: object, **_kwargs: object) -> None:
    return None


_UNDEFINED = object()

_install_module("voluptuous", Schema=_Schema, Required=lambda key: key,
                Optional=lambda key: key, ALLOW_EXTRA=object())
_install_module("homeassistant")
_install_module("homeassistant.components")
_install_module(
    "homeassistant.components.binary_sensor",
    BinarySensorDeviceClass=_BinarySensorDeviceClass,
    BinarySensorEntity=type("BinarySensorEntity", (), {}),
)
_install_module(
    "homeassistant.components.button",
    ButtonEntity=type("ButtonEntity", (), {}),
    ButtonEntityDescription=lambda **kwargs: SimpleNamespace(**kwargs),
)
_install_module(
    "homeassistant.components.number",
    NumberDeviceClass=_NumberDeviceClass,
    NumberEntity=type("NumberEntity", (), {}),
    NumberMode=_NumberMode,
)
_install_module(
    "homeassistant.components.sensor",
    SensorDeviceClass=_SensorDeviceClass,
    SensorStateClass=_SensorStateClass,
)
_install_module("homeassistant.config_entries", ConfigEntry=_ConfigEntry)
_install_module(
    "homeassistant.const",
    ATTR_HW_VERSION="hw_version",
    ATTR_MANUFACTURER="manufacturer",
    ATTR_MODEL="model",
    ATTR_SW_VERSION="sw_version",
    CONF_CLIENT_ID="client_id",
    CONF_CLIENT_SECRET="client_secret",
    CONF_PASSWORD="password",
    CONF_USERNAME="username",
    PERCENTAGE="%",
    Platform=_Platform,
    UnitOfTemperature=_UnitOfTemperature,
    UnitOfTime=_UnitOfTime,
)
_install_module("homeassistant.core", HomeAssistant=type("HomeAssistant", (), {}))
_install_module(
    "homeassistant.exceptions",
    ConfigEntryNotReady=type("ConfigEntryNotReady", (Exception,), {}),
    HomeAssistantError=type("HomeAssistantError", (Exception,), {}),
)
_install_module("homeassistant.helpers")
_install_module(
    "homeassistant.helpers.aiohttp_client",
    async_get_clientsession=lambda _hass: object(),
)
_install_module("homeassistant.helpers.config_validation", string=str)
_install_module("homeassistant.helpers.device_registry", async_get=lambda _hass: None)
_install_module("homeassistant.helpers.entity", DeviceInfo=_DeviceInfo)
_install_module("homeassistant.helpers.entity_platform", AddEntitiesCallback=object)
_install_module("homeassistant.helpers.httpx_client", get_async_client=lambda _hass: object())
_install_module("homeassistant.helpers.typing", ConfigType=dict, UNDEFINED=_UNDEFINED)
_install_module(
    "homeassistant.helpers.update_coordinator",
    CoordinatorEntity=_CoordinatorEntity,
    DataUpdateCoordinator=_DataUpdateCoordinator,
)

_install_module("custom_components.eight_sleep.pyEight.eight", EightSleep=_EightSleep)
_install_module(
    "custom_components.eight_sleep.pyEight.exceptions", RequestError=_RequestError
)
_install_module("custom_components.eight_sleep.pyEight.user", EightUser=_EightUser)
_install_module("custom_components.eight_sleep.device_actions")
_install_module(
    "custom_components.eight_sleep.util",
    create_offline_manager=lambda _hass, _entry: None,
    handle_api_error=_no_op_async,
)
_install_module(
    "custom_components.eight_sleep.health_check",
    async_setup_health_services=_no_op_async,
)
_install_module(
    "custom_components.eight_sleep.error_reporting",
    async_setup_error_reporting_services=_no_op_async,
)

import custom_components.eight_sleep as integration
from custom_components.eight_sleep import binary_sensor, button, number
from custom_components.eight_sleep.const import DOMAIN


NUMBER_ENTITY_TYPES = (
    "target_heating_level", "heating_level", "target_temperature",
    "current_temperature", "room_temperature", "water_level",
    "priming_progress", "firmware_version", "device_temperature",
    "device_humidity", "device_pressure", "sleep_duration", "sleep_latency",
    "sleep_efficiency", "sleep_quality", "sleep_score", "heart_rate",
    "respiratory_rate", "hrv_value", "presence_duration", "away_duration",
    "alarm_snooze_duration", "alarm_volume", "alarm_brightness",
    "notification_count", "alert_count", "error_count", "warning_count",
    "update_progress", "maintenance_progress", "analytics_score",
    "insights_score", "trends_score", "history_score", "settings_score",
    "configuration_score", "schedule_score", "routine_score",
)

DEVICE_NUMBER_ENTITY_TYPES = (
    "water_level", "priming_progress", "firmware_version",
    "device_temperature", "device_humidity", "device_pressure",
    "notification_count", "alert_count", "error_count", "warning_count",
    "update_progress", "maintenance_progress", "analytics_score",
    "insights_score", "trends_score", "history_score", "settings_score",
    "configuration_score", "schedule_score", "routine_score",
)

BINARY_SENSOR_TYPES = (
    "bed_presence", "away_mode_active", "device_online", "priming_needed",
    "is_priming", "has_water", "alarm_enabled", "alarm_ringing",
    "alarm_dismissed", "alarm_stopped", "sleep_tracking_enabled",
    "session_processing", "device_connected", "firmware_updating",
    "maintenance_required", "error_detected", "warning_active",
    "notification_pending", "alert_active", "update_available",
    "support_needed", "warranty_active", "analytics_enabled",
    "insights_available", "trends_available", "history_available",
    "settings_modified", "configuration_changed", "schedule_active",
    "routine_enabled",
)

DEVICE_BINARY_SENSOR_TYPES = (
    "device_online", "priming_needed", "is_priming", "has_water",
    "device_connected", "firmware_updating", "maintenance_required",
    "error_detected", "warning_active", "notification_pending", "alert_active",
    "update_available", "support_needed", "warranty_active",
    "analytics_enabled", "insights_available", "trends_available",
    "history_available", "settings_modified", "configuration_changed",
    "schedule_active", "routine_enabled",
)


class _FakeUser:
    def __init__(self) -> None:
        self.user_id = "user-001"
        self.side = "left"
        self.user_profile = {"firstName": "Taylor"}
        self.base_data: dict[str, object] = {}
        self.bed_presence = True
        self.target_heating_level = -2


class _FakeApi:
    def __init__(self, *, has_base: bool) -> None:
        self.device_id = "device-001"
        self.has_base = has_base
        self.is_pod = not has_base
        self.users = {"user-001": _FakeUser()}
        self.device_data = {
            "modelString": "Pod",
            "sensorInfo": {"hwRevision": "rev-a"},
            "firmwareVersion": "1.0",
        }
        self.device_update_count = 0
        self.user_update_count = 0
        self.base_update_count = 0

    @property
    def base_user(self) -> _FakeUser | None:
        return next(iter(self.users.values())) if self.has_base else None

    async def start(self) -> bool:
        return True

    async def update_device_data(self) -> dict[str, object]:
        self.device_update_count += 1
        return self.device_data

    async def update_user_data(self) -> dict[str, _FakeUser]:
        self.user_update_count += 1
        return self.users

    async def update_base_data(self) -> dict[str, object] | None:
        self.base_update_count += 1
        return self.base_user.base_data if self.base_user else None


class _FakeOfflineManager:
    async def initialize(self) -> None:
        return None

    def mark_connection_success(self) -> None:
        return None

    def mark_connection_error(self) -> None:
        return None

    async def get_data_with_fallback(
        self, _key: str, fetch: object, *args: object
    ) -> object:
        return await fetch(*args)


class _FakeDeviceRegistry:
    def __init__(self) -> None:
        self.created: list[dict[str, object]] = []

    def async_get_or_create(self, **values: object) -> None:
        self.created.append(values)


class _FakeConfigEntries:
    def __init__(self) -> None:
        self.forwarded: list[tuple[_ConfigEntry, list[str]]] = []

    async def async_forward_entry_setups(
        self, entry: _ConfigEntry, platforms: list[str]
    ) -> None:
        self.forwarded.append((entry, platforms))


class _FakeHass:
    def __init__(self) -> None:
        self.data: dict[str, object] = {}
        self.config = SimpleNamespace(time_zone="UTC")
        self.config_entries = _FakeConfigEntries()


def _platform_fixture(has_base: bool) -> tuple[object, _ConfigEntry, _FakeApi, object, object]:
    api = _FakeApi(has_base=has_base)
    entry = _ConfigEntry("entry-001", {"username": "fixture@example.invalid"})
    device_coordinator = object()
    user_coordinator = object()
    config_data = integration.EightSleepConfigEntryData(
        api=api,
        device_coordinator=device_coordinator,
        user_coordinator=user_coordinator,
        base_coordinator=object(),
    )
    hass = SimpleNamespace(data={DOMAIN: {entry.entry_id: config_data}})
    return hass, entry, api, device_coordinator, user_coordinator


class EntityPlatformSetupTests(unittest.IsolatedAsyncioTestCase):
    async def test_buttons_are_base_only_and_send_inverted_commands(self) -> None:
        hass, entry, api, _device_coordinator, _user_coordinator = _platform_fixture(True)
        calls: list[str] = []

        async def play() -> None:
            calls.append("play")

        async def pause() -> None:
            calls.append("pause")

        api.base_user.play_soundscape = play
        api.base_user.pause_soundscape = pause
        entities: list[object] = []
        await button.async_setup_entry(hass, entry, entities.extend)
        self.assertEqual(len(entities), 2)
        self.assertEqual(
            {entity._attr_unique_id for entity in entities},
            {"device-001.base.base_play_soundscape", "device-001.base.base_pause_soundscape"},
        )
        await entities[0].async_press()
        await entities[1].async_press()
        self.assertEqual(calls, ["play", "pause"])

        hass, entry, _api, _device_coordinator, _user_coordinator = _platform_fixture(False)
        entities = []
        await button.async_setup_entry(hass, entry, entities.extend)
        self.assertEqual(entities, [])

    async def test_number_setup_preserves_contract_for_base_and_pod_entries(self) -> None:
        """Number setup consumes canonical data and retains every registration."""
        for has_base in (True, False):
            with self.subTest(has_base=has_base):
                hass, entry, api, device_coordinator, user_coordinator = (
                    _platform_fixture(has_base)
                )
                entities: list[object] = []

                await number.async_setup_entry(hass, entry, entities.extend)

                user_entities = [
                    entity for entity in entities
                    if isinstance(entity, number.EightNumberEntity)
                ]
                device_entities = [
                    entity for entity in entities
                    if isinstance(entity, number.EightDeviceNumberEntity)
                ]
                self.assertEqual(
                    Counter(entity._entity_type for entity in user_entities),
                    Counter(NUMBER_ENTITY_TYPES),
                )
                self.assertEqual(
                    Counter(entity._entity_type for entity in device_entities),
                    Counter(DEVICE_NUMBER_ENTITY_TYPES),
                )
                device_backed = {
                    "presence_duration", "away_duration", "alarm_snooze_duration",
                    "alarm_volume", "alarm_brightness",
                }
                self.assertTrue(all(
                    entity.coordinator is (device_coordinator if entity._entity_type in device_backed else user_coordinator)
                    for entity in user_entities
                ))
                self.assertTrue(
                    all(entity.coordinator is device_coordinator for entity in device_entities)
                )
                self.assertTrue(
                    all(entity._user_obj is api.users["user-001"] for entity in user_entities)
                )
                self.assertTrue(all(entity._user_obj is None for entity in device_entities))
                self.assertEqual(
                    {entity._attr_unique_id for entity in user_entities},
                    {
                        f"device-001.user-001.{entity_type}"
                        for entity_type in NUMBER_ENTITY_TYPES
                    },
                )
                self.assertEqual(
                    {entity._attr_unique_id for entity in device_entities},
                    {
                        f"device-001.{entity_type}"
                        for entity_type in DEVICE_NUMBER_ENTITY_TYPES
                    },
                )
                target_heating = next(
                    entity
                    for entity in user_entities
                    if entity._entity_type == "target_heating_level"
                )
                self.assertEqual(target_heating.native_value, -2)
                self.assertEqual(
                    target_heating.extra_state_attributes,
                    {
                        "side": "left",
                        "user_id": "user-001",
                        "entity_type": "target_heating_level",
                    },
                )

    async def test_binary_setup_preserves_contract_for_base_and_pod_entries(self) -> None:
        """Binary setup consumes canonical data and retains every registration."""
        for has_base in (True, False):
            with self.subTest(has_base=has_base):
                hass, entry, api, device_coordinator, user_coordinator = (
                    _platform_fixture(has_base)
                )
                entities: list[object] = []

                await binary_sensor.async_setup_entry(hass, entry, entities.extend)

                user_entities = [
                    entity for entity in entities
                    if isinstance(entity, binary_sensor.EightBinarySensor)
                    and entity._sensor_type != "snoring_mitigation_active"
                ]
                device_entities = [
                    entity for entity in entities
                    if isinstance(entity, binary_sensor.EightDeviceBinarySensor)
                ]
                self.assertEqual(
                    Counter(entity._sensor_type for entity in user_entities),
                    Counter(BINARY_SENSOR_TYPES),
                )
                self.assertEqual(
                    Counter(entity._sensor_type for entity in device_entities),
                    Counter(DEVICE_BINARY_SENSOR_TYPES),
                )
                device_backed = {
                    "away_mode_active", "alarm_enabled", "alarm_ringing",
                    "alarm_dismissed", "alarm_stopped",
                }
                self.assertTrue(all(
                    entity.coordinator is (device_coordinator if entity._sensor_type in device_backed else user_coordinator)
                    for entity in user_entities
                ))
                self.assertTrue(
                    all(entity.coordinator is device_coordinator for entity in device_entities)
                )
                self.assertTrue(
                    all(entity._user_obj is api.users["user-001"] for entity in user_entities)
                )
                self.assertTrue(all(entity._user_obj is None for entity in device_entities))
                self.assertEqual(
                    {entity._attr_unique_id for entity in user_entities},
                    {
                        f"device-001.user-001.{sensor_type}"
                        for sensor_type in BINARY_SENSOR_TYPES
                    },
                )
                self.assertEqual(
                    {entity._attr_unique_id for entity in device_entities},
                    {
                        f"device-001.{sensor_type}"
                        for sensor_type in DEVICE_BINARY_SENSOR_TYPES
                    },
                )
                base_entities = [
                    entity for entity in entities
                    if getattr(entity, "_sensor_type", None) == "snoring_mitigation_active"
                ]
                self.assertEqual(len(base_entities), 1 if has_base else 0)
                bed_presence = next(
                    entity
                    for entity in user_entities
                    if entity._sensor_type == "bed_presence"
                )
                self.assertTrue(bed_presence.is_on)
                self.assertEqual(
                    bed_presence.extra_state_attributes,
                    {
                        "side": "left",
                        "user_id": "user-001",
                        "sensor_type": "bed_presence",
                    },
                )


class IntegrationSetupTests(unittest.IsolatedAsyncioTestCase):
    async def test_base_setup_registers_stable_device_with_optional_metadata(self) -> None:
        """Base setup registers its device even when hardware metadata is absent."""
        api = _FakeApi(has_base=True)
        hass = _FakeHass()
        entry = _ConfigEntry(
            "entry-001",
            {"username": "fixture@example.invalid", "password": "sanitized"},
        )
        offline_manager = _FakeOfflineManager()
        device_registry = _FakeDeviceRegistry()

        with (
            patch.object(integration, "EightSleep", new=lambda *_args, **_kwargs: api),
            patch.object(
                integration,
                "create_offline_manager",
                new=lambda _hass, _entry: offline_manager,
            ),
            patch.object(integration, "async_get", new=lambda _hass: device_registry),
        ):
            result = await integration.async_setup_entry(hass, entry)

        self.assertTrue(result)
        self.assertEqual(api.base_update_count, 1)
        config_data = hass.data[DOMAIN][entry.entry_id]
        self.assertEqual(config_data.base_coordinator.refresh_count, 1)
        base_device = next(
            device
            for device in device_registry.created
            if (DOMAIN, "device-001.base") in device["identifiers"]
        )
        self.assertEqual(base_device["via_device"], (DOMAIN, "device-001"))
        self.assertIs(base_device["model"], _UNDEFINED)
        self.assertIs(base_device["hw_version"], _UNDEFINED)
        self.assertIs(base_device["sw_version"], _UNDEFINED)

    async def test_pod_setup_never_fetches_or_registers_a_base(self) -> None:
        """Pod-only setup does not touch the unavailable Base capability."""
        api = _FakeApi(has_base=False)
        hass = _FakeHass()
        entry = _ConfigEntry(
            "entry-001",
            {"username": "fixture@example.invalid", "password": "sanitized"},
        )
        offline_manager = _FakeOfflineManager()
        device_registry = _FakeDeviceRegistry()

        with (
            patch.object(integration, "EightSleep", new=lambda *_args, **_kwargs: api),
            patch.object(
                integration,
                "create_offline_manager",
                new=lambda _hass, _entry: offline_manager,
            ),
            patch.object(integration, "async_get", new=lambda _hass: device_registry),
        ):
            result = await integration.async_setup_entry(hass, entry)

        self.assertTrue(result)
        self.assertEqual(api.device_update_count, 1)
        self.assertEqual(api.user_update_count, 1)
        self.assertEqual(api.base_update_count, 0)
        config_data = hass.data[DOMAIN][entry.entry_id]
        self.assertEqual(config_data.base_coordinator.refresh_count, 0)
        registered_identifiers = {
            identifier
            for device in device_registry.created
            for identifier in device["identifiers"]
        }
        self.assertNotIn((DOMAIN, "device-001.base"), registered_identifiers)


if __name__ == "__main__":
    unittest.main()
