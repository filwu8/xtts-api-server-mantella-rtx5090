#!/usr/bin/env python3
"""
XTTS API Server Launcher for Mantella
专为Mantella优化的XTTS API服务器启动器
"""

import os
import sys
import subprocess
import configparser
import time
import ctypes
import platform
from pathlib import Path

# 设置控制台标题和编码
if platform.system() == "Windows":
    ctypes.windll.kernel32.SetConsoleTitleW("XTTS API Server - Mantella")
    os.system('chcp 65001 > nul')  # 设置UTF-8编码

def print_banner():
    """打印启动横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    XTTS API Server - Mantella               ║
║                     语音合成API服务器                        ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_environment():
    """检查运行环境"""
    print("🔍 检查运行环境...")
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"   Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查虚拟环境
    venv_path = Path(".venv")
    if venv_path.exists():
        print("   ✅ 虚拟环境已找到")
        python_exe = venv_path / "Scripts" / "python.exe"
        if python_exe.exists():
            print(f"   ✅ Python解释器: {python_exe}")
            return str(python_exe)
        else:
            print("   ❌ 虚拟环境中未找到Python解释器")
            return None
    else:
        print("   ⚠️  未找到虚拟环境，使用系统Python")
        return sys.executable

def load_config():
    """加载配置文件"""
    print("📋 加载配置文件...")
    
    config_path = Path("config.ini")
    if not config_path.exists():
        print("   ❌ 未找到config.ini文件")
        return None
    
    config = configparser.ConfigParser()
    try:
        config.read(config_path, encoding='utf-8')
        print("   ✅ 配置文件加载成功")
        return config
    except Exception as e:
        print(f"   ❌ 配置文件加载失败: {e}")
        return None

def build_command(python_exe, config):
    """构建启动命令"""
    print("🔧 构建启动命令...")
    
    # 基础命令
    cmd = [python_exe, "-m", "xtts_api_server"]
    
    if config and 'DEFAULT' in config:
        default_config = config['DEFAULT']
        
        # 添加参数
        host = default_config.get('host', 'localhost')
        # 修正host配置错误（如果host是数字，说明配置有误）
        if host.isdigit():
            host = 'localhost'
            print(f"   ⚠️  配置文件中host设置有误（{default_config.get('host')}），使用默认值: {host}")
        
        port = default_config.get('port', '8020')
        device = default_config.get('device', 'cuda')
        speaker_folder = default_config.get('speakerfolder', 'speakers/')
        latent_speaker_folder = default_config.get('latentspeakerfolder', 'latent_speaker_folder/')
        output_folder = default_config.get('outputfolder', 'output/')
        model_folder = default_config.get('modelfolder', 'xtts_models/')
        model_version = default_config.get('modelversion', 'v2.0.2')
        listen = default_config.getboolean('listen', False)
        lowvram = default_config.getboolean('lowvram', False)
        deepspeed = default_config.getboolean('deepspeed', False)
        
        # 添加参数到命令
        cmd.extend(["-hs", host])
        cmd.extend(["-p", port])
        cmd.extend(["-d", device])
        cmd.extend(["-sf", speaker_folder])
        cmd.extend(["-lsf", latent_speaker_folder])
        cmd.extend(["-o", output_folder])
        cmd.extend(["-mf", model_folder])
        cmd.extend(["-v", model_version])
        
        if listen:
            cmd.append("--listen")
        if lowvram:
            cmd.append("--lowvram")
        if deepspeed:
            cmd.append("--deepspeed")
        
        print(f"   ✅ 启动参数配置完成")
        print(f"   📡 服务器地址: {host}:{port}")
        print(f"   🖥️  计算设备: {device}")
        print(f"   🔊 说话人文件夹: {speaker_folder}")
        print(f"   📁 输出文件夹: {output_folder}")
        print(f"   🤖 模型版本: {model_version}")
        if deepspeed:
            print(f"   ⚡ DeepSpeed加速: 已启用")
        if lowvram:
            print(f"   💾 低显存模式: 已启用")
    else:
        print("   ⚠️  使用默认配置启动")
    
    return cmd

def start_server(cmd):
    """启动服务器"""
    print("🚀 启动XTTS API服务器...")
    print("=" * 60)
    
    try:
        # 启动服务器进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print("✅ 服务器启动成功！")
        print("📖 API文档地址: http://localhost:8020/docs")
        print("🛑 按 Ctrl+C 停止服务器")
        print("=" * 60)
        
        # 实时输出日志
        for line in process.stdout:
            print(line.rstrip())
            
    except KeyboardInterrupt:
        print("\n🛑 收到停止信号，正在关闭服务器...")
        process.terminate()
        process.wait()
        print("✅ 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    try:
        # 打印横幅
        print_banner()
        
        # 检查环境
        python_exe = check_environment()
        if not python_exe:
            print("❌ 环境检查失败，无法启动")
            input("按任意键退出...")
            return
        
        # 加载配置
        config = load_config()
        
        # 构建命令
        cmd = build_command(python_exe, config)
        
        # 启动服务器
        start_server(cmd)
        
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        input("按任意键退出...")

if __name__ == "__main__":
    main()
