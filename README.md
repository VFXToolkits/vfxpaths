# vfxpaths
It is a system analysis framework related to VFX common file operations


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

## support environment

## todo

[x] Finish loading configuration file
[x] The completion path is divided into dictionaries according to rules
