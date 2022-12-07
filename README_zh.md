# vfxpaths
It is a system analysis framework related to VFX common file operations

## install

pip install vfxpaths

## config format

路径中包含的环境变量的表示方法： [ENV_NAME]
需要返回字段中映射的模板表示法：{field}
也可以不用在环境变量中存在，通过配置来配置特定路径读取

1. 配置文件可以通过环境变量来指定，并且初始启动的时候，优先级是最高的,环境变量`VFXPATHS_CONFIG_FILE`指向的值可以是具体的python数据，也可以是url地址，但必须是get，
其中的路径通用支持上述提到的环境变量来书写，当系统中存在这样的环境变量的时候会解析为真实的路径。

json的配置格式和说明：

```json
{"config_template": {"key": "value"},
  "windows_root_path": "",
  "mac_root_path": "",
  "linux_root_path": "",
  "custom_replaced_value": {"key": ""}
}
```

2. 通过类来配置，在当前运行的环境中存在全局实例变量名称为`VFX_paths_config`开头，并且实例中包含上诉字段即可。

注册模板的顺序按照上诉方式顺序执行，并且找到其中一种就停止查找。

## highlights

1. 在vfx工作中快速映射对应的路径到字典
2. 常用路径的解析，生成真实的路径
3. 常用文件或者json的读取
4. 模板配置比较灵活，可用多种方式来配置

## support environment

1. python3.7 以上版本

## todo

1. 完成配置文件加载
2. 完成路径按规则分割为字典
3. 常见文件的快速读写操作


## 简单使用

1. 模板匹配

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

输出值

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

2. 文件快速读取

```python
from vfxpaths import RW

json_class = RW(r"E:\demo_1")

# 读取 _setting.json结尾的文件

print(json_class.read_end_json("_setting.json"))
```

