#coding=utf-8


'''
requires Python 3.6 or later
pip install requests
'''
import base64
import json
import uuid
import requests

# 填写平台申请的appid, access_token以及cluster
appid = "6212223996"
access_token= "UmTfKeyRxQ1Nxl1LdB4GcyjZvYdkPcZX"
cluster = "volcano_tts"


voice_type = "zh_female_gaolengyujie_moon_bigtts"
host = "openspeech.bytedance.com"
api_url = f"https://{host}/api/v1/tts"

header = {"Authorization": f"Bearer;{access_token}"}

request_json = {
    "app": {
        "appid": appid,
        "token": "access_token",
        "cluster": cluster
    },
    "user": {
        "uid": "388808087185088"
    },
    "audio": {
        "voice_type": voice_type,
        "encoding": "wav",
        "speed_ratio": 1.0,
        "volume_ratio": 1.0,
        "pitch_ratio": 1.0,
    },
    "request": {
        "reqid": str(uuid.uuid4()),
        "text": "远方来的冒险者呐，若想探寻失落的遗迹，需先去寂静沼泽寻得古老钥匙，它能开启那通往未知宝藏的大门，在阴影中我们潜行，于无声处听惊雷。 剑的意志永存，龙裔，让德尔菲娜指引你前行。",
        "text_type": "plain",
        "operation": "query",
        "with_frontend": 1,
        "frontend_type": "unitTson"

    }
}

if __name__ == '__main__':
    try:
        resp = requests.post(api_url, json.dumps(request_json), headers=header)
        print(f"resp body: \n{resp.json()}")
        if "data" in resp.json():
            data = resp.json()["data"]
            file_to_save = open("test_submit.wav", "wb")
            file_to_save.write(base64.b64decode(data))
    except Exception as e:
        e.with_traceback()


