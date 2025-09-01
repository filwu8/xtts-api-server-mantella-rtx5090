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
appid = "5243181745"
access_token= "baEGElWbqPQe-uutErottu8dwOA8ppBC"
cluster = "volcano_icl"

# 转换文本文件
custext = "在每一场婚礼的璀璨画卷中，若说我们婚礼策划师是编织梦幻场景的工匠，那么 [小极] 老师便是那捕捉永恒瞬间的灵魂捕手。从仪式开始的神圣时刻，他如灵动的光影精灵，在人群缝隙间巧妙穿梭，却又丝毫不会惊扰现场的庄重与温馨。他的每一个步伐、每一次角度的转换，都精准得如同星辰在既定轨道运行。那专业的相机在他手中，仿佛不再是冰冷的器械，而是他延伸的感知器官，敏锐地捕捉着每一丝情感的涟漪。当新娘挽着父亲的手臂，带着对未来的憧憬与对过往的不舍，缓缓走向新郎时，他用镜头定格了父亲眼中闪烁的欣慰与不舍交织的复杂光芒，以及新娘脸颊上那幸福与紧张交融的动人红晕。那一瞬间，时间仿佛为他的镜头所停留，所有的爱与期待都被封印在那一方小小的画面之中。而到了敬酒环节，现场气氛热烈而欢腾，他又似一位冷静的观察者，在喧闹中迅速捕捉到新人与亲友们互动时那些充满温情与欢乐的画面。新人间不经意的对视，饱含着对未来相伴一生的坚定；长辈们那慈祥而开怀的笑容，是对新人最真挚的祝福写照。他用独特的视角与精湛的技艺，将这些稍纵即逝的美好，一一转化为可以触摸的珍贵回忆。在拍摄婚纱照时，他更是展现出了非凡的创意与耐心。无论是在阳光洒满的花海中，还是在夕阳余晖映照的古老城堡下，他都能引导新人自然地展现出最美好的姿态。他巧妙地运用光线，让每一张照片都像是从梦幻世界中截取的片段，新人的爱情在那光影交错间熠熠生辉。[小极] 老师的作品，不仅仅是简单的照片，而是一部部关于爱情的视觉史诗。他用镜头讲述着每一对新人独一无二的爱情故事，将那些稍纵即逝的美好瞬间，雕琢成永恒的璀璨星辰，镶嵌在每一对新人的爱情长河之中，让他们在岁月流转中，随时都能翻开这珍贵的记忆相册，重温婚礼当日的幸福满溢与甜蜜温馨。"

voice_type = "S_vfLlxfBj1"
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
        "encoding": "mp3",
        "speed_ratio": 1.0,
        "volume_ratio": 1.0,
        "pitch_ratio": 1.0,
    },
    "request": {
        "reqid": str(uuid.uuid4()),
        "text": custext,
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
            file_to_save = open("tts_http_demo.mp3", "wb")
            file_to_save.write(base64.b64decode(data))
    except Exception as e:
        e.with_traceback()
