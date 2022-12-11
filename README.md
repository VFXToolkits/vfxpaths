# vfxpaths
It is a system analysis framework related to VFX common file operations

中文文档查看readme_zh.md

## config format

Representation of environment variables included in the path: [ENV_NAME]
The template representation of the mapping in the field needs to be returned: {field}
It can also be configured to read a specific path without having to exist in the environment variable

1. The configuration file can be specified through the environment variable, and the priority is the highest when it is initially started. 
The environment variable 'VFXPATHS_ CONFIG_ The value pointed to by FILE 'can be specific python data or url address, but it must be get,
The path generally supports the environment variables mentioned above to write. When such environment variables exist in the system, 
they will be resolved to the real path.


Configuration format and description of json:

```json
{"config_template": {"key": "value"},
  "windows_root_path": "",
  "mac_root_path": "",
  "linux_root_path": "",
  "custom_replaced_value": {"key": ""}
}
```

2. Configure by class. In the current running environment, 
there is a global instance variable named 'VFX_ paths_ Config ', and the instance contains the appeal field.

The registration template is executed in the order of appeal, and the search will be stopped when one of them is found.

## highlights

1. Quickly mapping corresponding paths to dictionaries in VFX work
2. Parsing of common pathways to generate real pathways
3. Commonly used files or reads of a Simon
4. Template configuration is more flexible and can be configured in many ways

## How to use

1. Template matching

```python

import os
from vfxpaths import add_config_template, Resolve
import vfxpaths

add_config_template("key_name", 
                    r"{drive}/{project}/assets/{asset_name}/{assets_id}/{task_name}/{status}/{task_name}/{file_name}_{level}_{index}_v{version}.{filetype}")
vfxpaths.init_config()

os.environ["project_root"] = "Z:/PJ_1581892300583608320/assets/changjing"

path = "[project_root]/AS_158262777/moxingcaizhizonghezhizuo/approve/moxingcaizhizonghezhizuo/testzichan_eeee_01_v001.ma"

test = Resolve(target_path=path, use_name="test")

print(test.get_dict_data)

```

```json
{'drive': 'Z:',
 'project': 'PJ_1581892300583608320',
 'asset_name': 'changjing',
 'assets_id': 'AS_1582627772620505088',
 'task_name': 'moxingcaizhizonghezhizuo',
 'status': 'approve',
 'file_name': 'testzichan',
 'lod': 'eeee',
 'index': '01',
 'version': '001',
 'filetype': 'ma'}
```

2. Document rapid read and write

```python
from vfxpaths import RW

json_class = RW(r"E:\demo_1")

# Reads _Setting.jon ended papers

print(json_class.read_end_json("_setting.json"))
```

