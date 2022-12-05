# vfxpaths
It is a system analysis framework related to VFX common file operations


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

## support environment

## todo

[x] 完成配置文件加载
[x] 完成路径按规则分割为字典
