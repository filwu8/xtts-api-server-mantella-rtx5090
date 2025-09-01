# coding=utf-8
import asyncio
import websocket
import uuid
import json
import gzip
import copy
import sys
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor

# 定义消息类型、标志、序列化方法和压缩方法的映射
MESSAGE_TYPES = {10: "audio with textid response", 11: "audio-only server response", 15: "error message from server"}
MESSAGE_TYPE_SPECIFIC_FLAGS = {0: "no sequence number", 1: "sequence number > 0",
                               2: "last message from server (seq < 0)", 3: "sequence number < 0"}
MESSAGE_SERIALIZATION_METHODS = {0: "no serialization", 1: "JSON", 15: "custom type"}
MESSAGE_COMPRESSIONS = {0: "no compression", 1: "gzip", 15: "custom compression method"}

# 配置信息
appid = "xxx"
token = "xxx"
header = {"Authorization": f"Bearer; {token}"}
cluster = "xxx"
host = "openspeech.bytedance.com"
api_url = f"wss://{host}/api/v1/voice_conv/ws"

# 请求头定义
full_client_request_header = bytearray(b'\x11\x10\x10\x00')
audio_only_client_norm_request_header = bytearray(b'\x11\x21\x00\x00')
audio_only_client_last_request_header = bytearray(b'\x11\x23\x00\x00')

# 请求JSON模板
request_json = {
    "app": {
        "appid": 6212223996,
        "token": "UmTfKeyRxQ1Nxl1LdB4GcyjZvYdkPcZX",
        "cluster": "volcano_voice_conv"
    },
    "user": {
        "uid": "388808087185088"
    },
    "audio": {
        "voice": "other",
        "voice_type": "VC_BV001_streaming",  # 这个值将从Excel中读取
        "encoding": "wav",  # 修改为wav格式
        "speed": 10,
        "volume": 10,
        "pitch": 10,
        "rate": 16000,
        "compression_rate": 1
    },
    "request": {
        "reqid": "xxx",
        "operation": "xxx"
    }
}

class VCClient:
    def __init__(self, input_file, output_file, voice_type):
        self.reqid = str(uuid.uuid4())
        self.input_fs = open(input_file, "rb")
        self.output_fs = open(output_file, "wb")
        self.init_succ = False
        self.voice_type = voice_type

    def run(self):
        ws = websocket.WebSocketApp(api_url,
            header=header,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close)
        ws.run_forever()
        print("\nexit the connection...")

    def on_open(self, ws):
        print("\nconnect the server succ...")
        create_session(self.reqid, ws, self.voice_type)

    def on_message(self, ws, message):
        print("\nreceive message, len:%d" % len(message))
        done = parse_response(message, self.output_fs)
        if done:
            self.output_fs.close()
            print("\nclosing the connection...")
            ws.close()
            return
        if not self.init_succ:
            send_audio(self.reqid, ws, self.input_fs)
            self.init_succ = True

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("\nreceive close signal, closing the connection...")

def create_session(reqid, ws_cli, voice_type):
    submit_request_json = copy.deepcopy(request_json)
    submit_request_json["request"]["reqid"] = reqid
    submit_request_json["request"]["operation"] = "submit"
    submit_request_json["request"]["sequence"] = 1
    submit_request_json["audio"]["voice_type"] = voice_type  # 设置从Excel中读取的voice_type
    payload_bytes = str.encode(json.dumps(submit_request_json))
    full_client_request = bytearray(full_client_request_header)
    full_client_request.extend((len(payload_bytes)).to_bytes(4, 'big'))
    full_client_request.extend(payload_bytes)
    print("\n------------------------ test 'submit' -------------------------")
    print("request json: ", submit_request_json)
    print(full_client_request)
    ws_cli.send(full_client_request, websocket.ABNF.OPCODE_BINARY)
    print("\nfinish create session")

def send_audio(reqid, ws_cli, input_fs):
    print("\nstart to send audio to server")
    audio = input_fs.read()
    input_fs.close()
    pkg_size = 16000
    batch_cnt = int((len(audio) + pkg_size - 1) / pkg_size)
    idx = 0
    seq = 0
    if batch_cnt > 0:
        while True:
            if idx >= batch_cnt:
                break
            start = pkg_size * idx
            end = pkg_size * (idx + 1)
            if end > len(audio):
                end = len(audio)
            sub_audio = audio[start:end]
            seq = idx + 2
            if idx == batch_cnt - 1:
                seq = -1 * seq
            if seq > 0:
                audio_only_client_request = bytearray(audio_only_client_norm_request_header)
            else:
                audio_only_client_request = bytearray(audio_only_client_last_request_header)
            audio_only_client_request.extend(seq.to_bytes(4, 'big', signed=True))
            audio_only_client_request.extend(len(sub_audio).to_bytes(4, 'big'))
            audio_only_client_request.extend(sub_audio)
            ws_cli.send(audio_only_client_request, websocket.ABNF.OPCODE_BINARY)
            idx = idx + 1
    else:
        seq = -2
        sub_audio = ''
        audio_only_client_request = bytearray(audio_only_client_last_request_header)
        audio_only_client_request.extend(seq.to_bytes(4, 'big', signed=True))
        audio_only_client_request.extend(len(sub_audio).to_bytes(4, 'big'))
        print("\nsend auido header:", audio_only_client_request)
        ws_cli.send(audio_only_client_request, websocket.ABNF.OPCODE_BINARY)
        print("\nsend audio to server, len:%d" % len(sub_audio))
    input_fs.close()

def parse_response(res, file):
    print("--------------------------- response ---------------------------")
    protocol_version = res[0] >> 4
    header_size = res[0] & 0x0f
    message_type = res[1] >> 4
    message_type_specific_flags = res[1] & 0x0f
    serialization_method = res[2] >> 4
    message_compression = res[2] & 0x0f
    reserved = res[3]
    header_extensions = res[4:header_size * 4]
    payload = res[header_size * 4:]
    print(f"            Protocol version: {protocol_version:#x} - version {protocol_version}")
    print(f"                 Header size: {header_size:#x} - {header_size * 4} bytes ")
    print(f"                Message type: {message_type:#x} - {MESSAGE_TYPES[message_type]}")
    print(f" Message type specific flags: {message_type_specific_flags:#x} - {MESSAGE_TYPE_SPECIFIC_FLAGS[message_type_specific_flags]}")
    print(f"Message serialization method: {serialization_method:#x} - {MESSAGE_SERIALIZATION_METHODS[serialization_method]}")
    print(f"         Message compression: {message_compression:#x} - {MESSAGE_COMPRESSIONS[message_compression]}")
    print(f"                    Reserved: {reserved:#04x}")
    if header_size != 1:
        print(f"           Header extensions: {header_extensions}")
    if message_type == 0xb:  # audio-only server response
        if message_type_specific_flags == 0:  # no sequence number as ACK
            print("                Payload size: 0")
            return False
        else:
            sequence_number = int.from_bytes(payload[:4], "big", signed=True)
            payload_size = int.from_bytes(payload[4:8], "big", signed=False)
            payload = payload[8:]
            print(f"             Sequence number: {sequence_number}")
            print(f"                Payload size: {payload_size} bytes")
        file.write(payload)
        if sequence_number < 0:
            return True
        else:
            return False
    elif message_type == 0xf:
        code = int.from_bytes(payload[:4], "big", signed=False)
        msg_size = int.from_bytes(payload[4:8], "big", signed=False)
        error_msg = payload[8:]
        if message_compression == 1:
            error_msg = gzip.decompress(error_msg)
        error_msg = str(error_msg, "utf-8")
        print(f"          Error message code: {code}")
        print(f"          Error message size: {msg_size} bytes")
        print(f"               Error message: {error_msg}")
        return True
    else:
        print("undefined message type!")
        return True

def process_voice_type(input_file, output_dir, voice_type, language, voice_name, index):
    output_file = os.path.join(output_dir, f"{index}_{voice_name}_{language}_{voice_type}.wav")
    vc_cli = VCClient(input_file, output_file, voice_type)
    vc_cli.run()

def main():
    input_file = sys.argv[1]
    excel_file = "wsvoice.xls"  # Excel文件路径
    output_dir = "vc_ws_voiceprint"  # 输出文件夹

    # 创建输出文件夹
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 读取Excel文件
    df = pd.read_excel(excel_file)

    # 使用线程池并发执行
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for _, row in df.iterrows():
            index = row['序号']
            voice_name = row['音色名称']
            language = row['语种']
            voice_type = row['Voice_type']
            futures.append(executor.submit(process_voice_type, input_file, output_dir, voice_type, language, voice_name, index))
        
        # 等待所有任务完成
        for future in futures:
            future.result()

if __name__ == '__main__':
    websocket.enableTrace(False)
    main()