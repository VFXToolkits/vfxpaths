from vfxpaths import Entity, Resolve, add_config_template

add_config_template("test_name", 
                    r"{drive}/{project}/assets/{assets_type}/{asset_name}/{stage}/{task_name}/{version}")
aaatest = Resolve(target_path=r"O:\KLDTest\assets\env\iajgknkf_0e\mod\mod_high\v002", use_name="test_name")

test = Entity(aaatest.target_path)
config = test.rule_config()
config.map_key = aaatest.get_dict_data
# config.entity_name = aaatest.get_dict_data.get("asset_name")
config.extend = "usd"
# # config.custom_name = "mod_high"
config.rule_format.assets = {"name": r"{asset_name}.{task_name}.{extend}", "path": "maya/files"}

assets_path = test.full_path("assets")

print(assets_path)



