#coding=utf-8


'''
requires Python 3.6 or later
pip install requests
'''
import os
import base64
import json
import uuid
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# 填写平台申请的appid, access_token以及cluster
appid = "6212223996"
access_token= "UmTfKeyRxQ1Nxl1LdB4GcyjZvYdkPcZX"
cluster = "volcano_tts"

host = "openspeech.bytedance.com"
api_url = f"https://{host}/api/v1/tts"
header = {"Authorization": f"Bearer;{access_token}"}


# 创建voiceprint子目录（如果不存在）
output_dir = 'voiceprint'
os.makedirs(output_dir, exist_ok=True)



# 读取Excel文件
df = pd.read_excel('batch-run.xls')  # 根据实际文件名和路径调整

def process_voice_type(row):
    voice_type = row['Voice_type']  # 假设列名为Voice_type，请根据实际情况调整
    id = str(row['ID'])  # 假设有一个列名为ID用于生成文件名
    scene = str(row['推荐场景'])  # 假设有一个列名为推荐场景用于生成文件名
    language = str(row['语种'])  # 假设有一个列名为语种用于生成文件名
    voiceprint = str(row['音色名称'])   #音色名称

    request_json = {
        "app": {
            "appid": appid,
            "token": access_token,
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
            "text": "远方来的冒险者呐，若想探寻失落的遗迹，需先去寂静沼泽寻得古老钥匙，它能开启那通往未知宝藏的大门，在阴影中我们潜行，于无声处听惊雷。剑的意志永存，龙裔，让德尔菲娜指引你前行。",
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson"
        }
    }

    try:
        resp = requests.post(api_url, data=json.dumps(request_json), headers=header)
        if "data" in resp.json():
            data = resp.json()["data"]
            file_name = os.path.join(output_dir, f"{id}_{voiceprint}_{scene}_{language}_{voice_type}.wav")  # 使用子目录并格式化文件名
            with open(file_name, "wb") as file_to_save:
                file_to_save.write(base64.b64decode(data))
            return f"File saved: {file_name}"
        else:
            return f"Error processing {voice_type}: No data in response."
    except Exception as e:
        return f"Error processing {voice_type}: {e}"

# 使用线程池并发执行
with ThreadPoolExecutor(max_workers=10) as executor:  # 控制最大并发数为10
    future_to_row = {executor.submit(process_voice_type, row): row for index, row in df.iterrows()}
    for future in as_completed(future_to_row):
        row = future_to_row[future]
        try:
            print(future.result())
        except Exception as exc:
            print(f"Row generated an exception: {exc}")