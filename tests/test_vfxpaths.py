import os
import unittest
import sys

import vfxpaths
from tests.config_data.config_data import ConfigTest


class TestVfxpaths(unittest.TestCase):
    vfxpaths.maps_config_field(ConfigTest)

    @unittest.skipIf(sys.platform != "win32", "windows system usd")
    def test_windows_get_root_path(self):
        """test get config path"""
        get_root_path = vfxpaths.get_root_path()
        self.assertEqual(get_root_path, "D:/project/work")

    def test_path_is_replace(self):
        os.environ["VFXPATHS_GLOBAL_REPLACE"] = "1"
        get_root_path = vfxpaths.get_root_path()
        self.assertEqual(get_root_path, "z:/project/work")
        del os.environ["VFXPATHS_GLOBAL_REPLACE"]

    @classmethod
    def tearDownClass(cls) -> None:
        print("test TestVfxpaths end")


