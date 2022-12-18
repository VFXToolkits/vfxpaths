import os
import unittest
import sys

import vfxpaths
from tests.config_data.config_data import ConfigTest


class TestPath(unittest.TestCase):
    vfxpaths.maps_config_field(ConfigTest)

    def test_change_extension(self):
        """test replace Path Suffix"""
        get_path = vfxpaths.Path(r"E:\Grab.png")
        self.assertEqual(get_path.change_extension(".jpg"), "E:/Grab.jpg")

    def test_path_combine(self):
        get_path = vfxpaths.Path(r"E:\Users\look_dev_tool")
        self.assertEqual(get_path.combine("test"), "E:/Users/look_dev_tool/test")

    def test_list_path_combine(self):
        get_path = vfxpaths.Path(r"E:\Users\look_dev_tool")
        self.assertEqual(get_path.combine(["test", "a", "b"]), "E:/Users/look_dev_tool/test/a/b")

    @unittest.skipIf(sys.platform != "win32", "windows system usd")
    def test_env_path_combine(self):
        get_path = vfxpaths.Path(r"[windir]/test")
        self.assertEqual(get_path.combine("abc"), "C:/Windows/test/abc")

    def test_fallback_dir(self):
        get_path = vfxpaths.Path(r"E:\Users\look_dev_tool")
        self.assertEqual(get_path.fallback_dir(1), "E:/Users")

    def test_header_directory(self):
        get_path = vfxpaths.Path(r"E:\Users\look_dev_tool")
        self.assertEqual(get_path.header_directory(4), "E:/Users/look_dev_tool")

    @classmethod
    def tearDownClass(cls) -> None:
        print("test TestPath end")


