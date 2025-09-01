import requests

url = "https://api.siliconflow.cn/v1/audio/voice/deletions"
headers = {
    "Authorization": "Bearer sk-rdvjnyivjcznmujssqehrybbxsslcpvlbonycsacocrrqwvs",
    "Content-Type": "application/json"
}
payload = {
    "uri": "speech:wangziheng:w0jmbrd3xo:vbkjkocpgjdotscuxvtd"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.status_code)
print(response.text) #打印响应内容