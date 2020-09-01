import json
import requests

user_info = {}
user_info['strategy'] = ["idc_distance", "idc_isp", "idc_random", "specify_region", "vendor222_region"]
user_info['vendor_region'] = [{"appid":"e3febcf38cd647ecb400fe787e140880","region":"guangzhou-cmcc","vid":130451}]
user_info['worker_role'] = "subscriber"
user_info['random_distance'] = "100;500;1000"
user_info['converge_key_list'] = ["appId","cname","uid"]
user_info['converge_strategy'] = "strong_converge"
user_info['service_name'] = "mix_streaming"
user_info['env_conf'] = "/etc/voice/mix_streaming-env.json"
user_info["serve_sdk_port"] = 36003
user_info['serve_edge_port'] = 4318
user_info['audio_expire_time'] = 720
user_info['video_expire_time'] = 720
user_info['lbs_key'] = "0dd64736f41913475ea1f7b845a6a4e0606c82e6d59d38d342a8f1263ae029ab"
headers = {'content-type': 'application/json'}

r = requests.post("http://10.63.0.221:54545/app_center/v1/update_config?config_file=data.json", data=json.dumps(user_info), headers = headers)

print(r.headers)
print(r.json())
