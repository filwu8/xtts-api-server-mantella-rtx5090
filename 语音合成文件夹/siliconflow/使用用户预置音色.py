from pathlib import Path
from openai import OpenAI

speech_file_path = Path(__file__).parent / "speech:wangziheng:w0jmbrd3xo:qbyhyvpgwiggqccefely.mp3"

client = OpenAI(
    api_key="sk-rdvjnyivjcznmujssqehrybbxsslcpvlbonycsacocrrqwvs", # 从 https://cloud.siliconflow.cn/account/ak 获取
    base_url="https://api.siliconflow.cn/v1"
)

with client.audio.speech.with_streaming_response.create(
  model="FunAudioLLM/CosyVoice2-0.5B", # 支持 fishaudio / GPT-SoVITS / CosyVoice2-0.5B 系列模型
  voice="speech:wangziheng:w0jmbrd3xo:qbyhyvpgwiggqccefely", # 用户上传音色名称，参考
  # 用户输入信息
  input=" 请问你能模仿粤语的口音吗？< |endofprompt| >多保重，早休息。",
  response_format="mp3"
) as response:
    response.stream_to_file(speech_file_path)