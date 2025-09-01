import requests
url = "https://api.siliconflow.cn/v1/audio/voice/list"

headers = {
    "Authorization": "Bearer sk-rdvjnyivjcznmujssqehrybbxsslcpvlbonycsacocrrqwvs" # 从https://cloud.siliconflow.cn/account/ak获取
}
response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json()) # 打印响应内容（如果是JSON格式）