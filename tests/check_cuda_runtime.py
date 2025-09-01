#!/usr/bin/env python3
"""
CUDA/CPU 运行时检测脚本
- 打印 PyTorch CUDA 可用性
- 打印当前设备与可用 GPU 列表
- 调用服务端 /speakers_list 和一次最小 TTS 生成验证
"""

import os
import sys
import json
import time

import requests

try:
    import torch
except Exception as e:
    torch = None

BASE_URL = os.environ.get("XTTS_BASE_URL", "http://localhost:8020")


def check_torch_env():
    print("=== PyTorch 环境检查 ===")
    if torch is None:
        print("torch: 未安装或导入失败")
        return False
    print("torch.version:", getattr(torch, "__version__", "unknown"))
    print("torch.cuda.is_available():", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("torch.version.cuda:", getattr(torch.version, "cuda", None))
        print("可用GPU数量:", torch.cuda.device_count())
        for i in range(torch.cuda.device_count()):
            print(f"  - GPU[{i}]:", torch.cuda.get_device_name(i))
        try:
            t = torch.zeros((1,), device="cuda")
            print("CUDA 张量测试设备:", t.device)
        except Exception as e:
            print("CUDA 张量测试失败:", e)
    else:
        print("当前将回退为 CPU")
    return True


def check_api_endpoints():
    print("\n=== API 端点检查 ===")
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        print("/health:", r.status_code)
    except Exception as e:
        print("/health 请求失败:", e)
        return False

    try:
        r = requests.get(f"{BASE_URL}/speakers_list", timeout=10)
        print("/speakers_list:", r.status_code)
        data = r.json()
        # 简短打印结构
        if isinstance(data, dict):
            some_lang = next(iter(data.keys()), None)
            preview = data.get(some_lang)
            print("speakers_list结构示例:", some_lang, "->", str(preview)[:120], "...")
        else:
            print("speakers_list返回非字典:", type(data).__name__)
    except Exception as e:
        print("/speakers_list 请求失败:", e)
        return False

    return True


def minimal_tts_test():
    print("\n=== 最小TTS生成测试 ===")
    payload = {
        "text": "你好，GPU检测测试。",
        "speaker_wav": "malenord",
        "language": "zh-cn"
    }
    try:
        t0 = time.time()
        r = requests.post(f"{BASE_URL}/tts_to_audio/", json=payload, timeout=30)
        dt = time.time() - t0
        print("/tts_to_audio:", r.status_code, f"耗时: {dt:.2f}s")
        if r.status_code == 200:
            print("音频字节:", len(r.content))
            return True
        else:
            print("响应正文:", r.text[:200])
            return False
    except Exception as e:
        print("/tts_to_audio 请求失败:", e)
        return False


if __name__ == "__main__":
    ok_torch = check_torch_env()
    ok_api = check_api_endpoints()
    if ok_api:
        minimal_tts_test()

