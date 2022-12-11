## 完整使用教程

### json配置模板

配置1

```json
{"config_template": {"base_test": "{root}/{project}/{project_name}/{type}/{sq_name}/{shot_name}/{sq_name}_{shot_name}_v{version}.{ext}"},
  "windows_root_path": "D:/project/work",
  "mac_root_path": "/home/user_name/project/work",
  "linux_root_path": "/home/user_name/project/work",
  "custom_replaced_value": {"windows_root": "x:"},
  "custom_root_path": {"local_work_path": {"linux": "/home/name/work", "windows": "D:/project/work"}},
  "global_str_mapping": {"current_project_server": {"windows": "z:/project", "linux": "/project/name"}}
}
```

配置2
```json
{"config_template": {"base_test": "[custom_root_path.local_work_template]/{type}/{sq_name}/{shot_name}/{sq_name}_{shot_name}_v{version}.{ext}"},
  "windows_root_path": "D:/project/work",
  "mac_root_path": "/home/user_name/project/work",
  "linux_root_path": "/home/user_name/project/work",
  "custom_replaced_value": {"windows_root": "x:"},
  "custom_root_path": {"local_work_path": {"linux": "/home/name/work", 
    "windows": "D:/project/work"},
  "local_work_template": {"linux": "{project}/{name}", "windows": "{root}/{project}/{project_name}"}
  },
  "global_str_mapping": {"current_project_server": {"windows": "z:/project", "linux": "/project/name"}}
}
```
其中的[local_work_template]表示的需要替换的字段


## 路径映射

1. 简单的使用

在开始之前首先需要指定配置文件，方法有以下几种

* 环境变量方式注册配置1

set VFXPATHS_CONFIG_FILE={directory}/config1.json
其中directory表示的是你的json存放目录

* 通过手动的方式传入

```python
import vfxpaths

vfxpaths.register_config_file("{directory}/config1.json")
```

* 通过字典的方式传入

```python
import vfxpaths

# 把json的内容写入到字典中
config_dict = {"windows_root_path": "D:/project/work"}

vfxpaths.register_config(config_dict)
```

* 通过类的方式传入

```python
import vfxpaths

class ConfigTest:
    config_template = {"base_test": "{root}/{project}/{project_name}/{type}/{sq_name}/{shot_name}/{sq_name}_{shot_name}_v{version}.{ext}"}
    windows_root_path: str = "D:/project/work"
    mac_root_path: str = "/home/user_name/project/work"
    linux_root_path: str = "/home/user_name/project/work"
    custom_replaced_value = {"windows_root": "x:"}
    custom_root_path = {"local_work_path": {"linux": "/home/name/work"}}
    global_str_mapping = {"D:/project": {"windows": "z:/project", "linux": "/project"}}

vfxpaths.maps_config_field(ConfigTest)

```


## 路径解析

1. 例如使用了配置1的json

```python
import vfxpaths

vfxpaths.maps_config_field(ConfigTest)
```

获取给定路径映射成字典类型

```python

```
return

```text
{'root': 'Z:', 
'project': 'project', 
'project_name': 'PJ_158189', 
'type': 'shots', 
'sq_name': 'sq001', 
'shot_name': 'sh010', 
'version': '002', 
'ext': 'ma'}
```

各地一个字典或者json，映射为路径

```python
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
```
return

```text
"Z:/project/PJ_158189/shots/sq001/sh010/sq001_sh010_v002.ma"
```

## 文件的快速读写

例如 json文件

```python
from vfxpaths import RW

json_class = RW(r"E:\demo_1")

# 读取 _setting.json结尾的文件

print(json_class.read_end_json("_setting.json"))
```

