import requests

url = "https://api.siliconflow.cn/v1/uploads/audio/voice"
headers = {
    "Authorization": "Bearer sk-rdvjnyivjcznmujssqehrybbxsslcpvlbonycsacocrrqwvs" # 从 https://cloud.siliconflow.cn/account/ak 获取
}
files = {
    "file": open("校园里.mp3", "rb") # 参考音频文件
}
data = {
    "model": "FunAudioLLM/CosyVoice2-0.5B", # 模型名称
    "customName": "wangziheng", # 参考音频名称
    "text": "清晨，阳光轻柔地穿过淡薄的云层，纷纷扬扬地落在校园里。瞧啊，那棵古老的银杏，金黄的叶子在微风中轻轻摇曳，似在诉说着往昔的故事。“一年好景君须记，最是橙黄橘绿时。” 这般美好的秋日，怎能不让人心生欢喜？同学们，快来，咱们一起在这如画的校园里，开启充满活力的一天！嘿，你听，鸟儿欢快地歌唱，仿佛也在为这美好的时光欢呼。此刻，大家的笑声、读书声交织在一起，构成了一曲美妙的乐章。" # 参考音频的文字内容
}

response = requests.post(url, headers=headers, files=files, data=data)

print(response.status_code)
print(response.json())  # 打印响应内容（如果是JSON格式）