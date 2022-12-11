
class ConfigTest:
    config_template = {"base_test": "{root}/{project}/{project_name}/{type}/{sq_name}/{shot_name}/{sq_name}_{shot_name}_v{version}.{ext}"}
    windows_root_path: str = "D:/project/work"
    mac_root_path: str = "/home/user_name/project/work"
    linux_root_path: str = "/home/user_name/project/work"
    custom_replaced_value = {"windows_root": "x:"}
    custom_root_path = {"local_work_path": {"linux": "/home/name/work"}}
    global_str_mapping = {"D:/project": {"windows": "z:/project", "linux": "/project"}}

