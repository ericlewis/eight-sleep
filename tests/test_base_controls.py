import asyncio
import importlib.util
import pathlib
import sys
import types
import unittest

pkg = types.ModuleType("custom_components.eight_sleep")
pkg.__path__ = [str(pathlib.Path(__file__).parents[1] / "custom_components/eight_sleep")]
sys.modules.setdefault("custom_components.eight_sleep", pkg)
spec = importlib.util.spec_from_file_location(
    "custom_components.eight_sleep.pyEight.user",
    pathlib.Path(__file__).parents[1] / "custom_components/eight_sleep/pyEight/user.py",
)
user_module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = user_module
spec.loader.exec_module(user_module)
EightUser = user_module.EightUser


class FakeDevice:
    has_base = True
    device_id = "device-1"

    def __init__(self):
        self.calls = []

    async def api_request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return None


class BaseControlTests(unittest.TestCase):
    def test_angle_payload_is_paired_and_refreshes_without_legacy_fields(self):
        device = FakeDevice()
        user = EightUser(device, "user-1", "left")
        user._base_data = {"left": {"leg": {"currentAngle": 10}, "torso": {"currentAngle": 2}}}
        refreshed = []
        async def refresh():
            refreshed.append(True)
        user.update_base_data = refresh
        asyncio.run(user.set_base_angle(12, 4))
        payload = device.calls[0][2]["data"]
        self.assertEqual(payload, {"legAngle": 12, "torsoAngle": 4})
        self.assertTrue(refreshed)

    def test_preset_payload_includes_snore_mitigation(self):
        device = FakeDevice()
        user = EightUser(device, "user-1", "left")
        refreshed = []
        async def refresh():
            refreshed.append(True)
        user.update_base_data = refresh
        asyncio.run(user.set_base_preset("sleep"))
        self.assertEqual(device.calls[0][2]["data"], {"preset": "sleep", "snoreMitigation": False})
        self.assertTrue(refreshed)

    def test_soundscape_commands_use_inverted_api_states(self):
        device = FakeDevice()
        user = EightUser(device, "user-1", "left")
        asyncio.run(user.play_soundscape())
        asyncio.run(user.pause_soundscape())
        self.assertEqual(
            [(call[0], call[1]) for call in device.calls],
            [("PUT", "https://app-api.8slp.net/v1/users/user-1/audio/player/state"),
             ("PUT", "https://app-api.8slp.net/v1/users/user-1/audio/player/state")],
        )
        self.assertEqual(device.calls[0][2]["data"], {"state": "paused"})
        self.assertEqual(device.calls[1][2]["data"], {"state": "playing"})


if __name__ == "__main__":
    unittest.main()
