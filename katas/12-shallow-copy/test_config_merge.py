import copy
import unittest

import config_merge
from config_merge import tenant_config


class TestTenantConfig(unittest.TestCase):
    def setUp(self):
        self._snapshot = copy.deepcopy(config_merge.DEFAULTS)

    def tearDown(self):
        config_merge.DEFAULTS.clear()
        config_merge.DEFAULTS.update(copy.deepcopy(self._snapshot))

    def test_applies_nested_overrides(self):
        cfg = tenant_config({"db": {"host": "db.acme.io"}})
        self.assertEqual(cfg, {"db": {"host": "db.acme.io", "port": 5432}, "debug": False})

    def test_top_level_override(self):
        self.assertTrue(tenant_config({"debug": True})["debug"])

    def test_defaults_are_never_modified(self):
        tenant_config({"db": {"host": "db.acme.io"}})
        self.assertEqual(config_merge.DEFAULTS["db"]["host"], "localhost")

    def test_the_next_tenant_gets_clean_defaults(self):
        tenant_config({"db": {"host": "db.acme.io"}})
        other = tenant_config({})
        self.assertEqual(other["db"]["host"], "localhost")


if __name__ == "__main__":
    unittest.main()
