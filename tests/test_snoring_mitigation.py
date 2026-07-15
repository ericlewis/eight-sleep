import asyncio
import importlib.util
import pathlib
import sys
import types
import unittest

pkg = types.ModuleType("custom_components.eight_sleep")
pkg.__path__ = [str(pathlib.Path(__file__).parents[1] / "custom_components/eight_sleep")]
sys.modules.setdefault("custom_components.eight_sleep", pkg)
spec = importlib.util.spec_from_file_location("custom_components.eight_sleep.pyEight.user", pathlib.Path(__file__).parents[1] / "custom_components/eight_sleep/pyEight/user.py")
mod = importlib.util.module_from_spec(spec); sys.modules[spec.name] = mod; spec.loader.exec_module(mod)
if sys.modules.get("custom_components.eight_sleep") is pkg:
    del sys.modules["custom_components.eight_sleep"]

class Device:
    has_base = True
    def __init__(self): self.calls = []
    async def api_request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        if method == "GET": return {"snoringMitigation": {"enabled": True, "mitigationLevel": "medium"}}
        return None

class SnoringTests(unittest.TestCase):
    def test_refresh_and_atomic_write(self):
        d = Device(); u = mod.EightUser(d, "u", "left")
        asyncio.run(u.update_snoring_mitigation())
        self.assertEqual(u.snoring_mitigation, {"enabled": True, "mitigationLevel": "medium"})
        asyncio.run(u.set_snoring_mitigation(False, "medium"))
        self.assertEqual(d.calls[1][2]["data"], {"snoringMitigation": {"enabled": False, "mitigationLevel": "medium"}})

    def test_invalid_level_preserves_cache(self):
        d = Device(); u = mod.EightUser(d, "u", "left")
        u._snoring_mitigation = {"enabled": True, "mitigationLevel": "low"}
        with self.assertRaises(ValueError): asyncio.run(u.set_snoring_mitigation(False, "invalid"))
        self.assertEqual(u.snoring_mitigation["mitigationLevel"], "low")
