#!/usr/bin/env python3
"""
简化版构建脚本 - 构建XTTS API Server可执行文件
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """主函数"""
    print("=" * 60)
    print("    XTTS API Server - Mantella 可执行文件构建工具")
    print("=" * 60)
    
    # 检查源文件
    if not os.path.exists("xtts_launcher.py"):
        print("❌ 未找到源文件 xtts_launcher.py")
        input("按任意键退出...")
        return
    
    # 检查虚拟环境
    venv_path = Path(".venv")
    if venv_path.exists():
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
        pyinstaller_exe = venv_path / "Scripts" / "pyinstaller.exe"
        
        if python_exe.exists():
            print("✅ 找到虚拟环境")
            
            # 安装PyInstaller（如果需要）
            if not pyinstaller_exe.exists():
                print("📦 安装PyInstaller...")
                try:
                    subprocess.run([str(pip_exe), "install", "pyinstaller"], check=True)
                    print("✅ PyInstaller安装成功")
                except subprocess.CalledProcessError as e:
                    print(f"❌ PyInstaller安装失败: {e}")
                    input("按任意键退出...")
                    return
            
            # 构建命令
            cmd = [
                str(pyinstaller_exe),
                "--onefile",
                "--console",
                "--name", "xtts-api-server-mantella",
                "--clean",
                "xtts_launcher.py"
            ]
        else:
            print("❌ 虚拟环境不完整")
            input("按任意键退出...")
            return
    else:
        print("⚠️  未找到虚拟环境，使用系统Python")
        # 使用系统Python
        cmd = [
            "pyinstaller",
            "--onefile",
            "--console", 
            "--name", "xtts-api-server-mantella",
            "--clean",
            "xtts_launcher.py"
        ]
    
    # 执行构建
    print("🔨 开始构建...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ 构建成功！")
        
        # 检查输出文件
        exe_path = Path("dist") / "xtts-api-server-mantella.exe"
        if exe_path.exists():
            print(f"📁 可执行文件: {exe_path.absolute()}")
            print(f"📏 文件大小: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
    except FileNotFoundError:
        print("❌ 未找到pyinstaller，请先安装: pip install pyinstaller")
    
    input("按任意键退出...")

if __name__ == "__main__":
    main()
