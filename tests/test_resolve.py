import unittest
import vfxpaths
from vfxpaths import Resolve
from tests.config_data.config_data import ConfigTest


class TestResolve(unittest.TestCase):
    vfxpaths.maps_config_field(ConfigTest)

    @classmethod
    def setUpClass(cls):
        print("start test")
    
    @classmethod
    def tearDownClass(cls):
        print("end test")
    
    def test_get_target_path(self):
        self.resolve = Resolve(target_path="O:/")
        self.assertEqual(self.resolve.get_target_path, "O:/")

    def test_map_path(self):
        resolve = Resolve(target_path="Z:/project/PJ_158189/shots/sq001/sh010/sq001_sh010_v002.ma",
                          use_name="base_test")
        get_value = {'root': 'Z:',
                     'project': 'project',
                     'project_name': 'PJ_158189',
                     'type': 'shots',
                     'sq_name': 'sq001',
                     'shot_name': 'sh010',
                     'version': '002',
                     'ext': 'ma'}
        self.assertEqual(resolve.get_dict_data, get_value)

    def test_field_get(self):
        resolve = Resolve(target_path="Z:/project/PJ_158189/shots/sq001/sh010/sq001_sh010_v002.ma",
                          use_name="base_test")

        self.assertEqual(len(resolve.get_fields_only_list), 8)

    def test_field_to_path(self):
        resolve = Resolve(use_name="base_test")
        get_value = {'root': 'Z:',
                     'project': 'project',
                     'project_name': 'PJ_158189',
                     'type': 'shots',
                     'sq_name': 'sq001',
                     'shot_name': 'sh010',
                     'version': '002',
                     'ext': 'ma'}
        current_path = resolve.dict_to_path(get_value)
        self.assertEqual(current_path, "Z:/project/PJ_158189/shots/sq001/sh010/sq001_sh010_v002.ma")

