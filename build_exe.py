#!/usr/bin/env python3
"""
构建XTTS API Server可执行文件的脚本
使用PyInstaller将Python脚本编译为exe文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
        return True
    except ImportError:
        print("❌ PyInstaller未安装")
        return False

def install_pyinstaller():
    """安装PyInstaller"""
    print("📦 正在安装PyInstaller...")
    try:
        # 检查是否在虚拟环境中
        venv_path = Path(".venv")
        if venv_path.exists():
            python_exe = venv_path / "Scripts" / "python.exe"
            pip_exe = venv_path / "Scripts" / "pip.exe"
            if python_exe.exists() and pip_exe.exists():
                print("   使用虚拟环境安装...")
                subprocess.run([str(pip_exe), "install", "pyinstaller"], check=True)
            else:
                print("   虚拟环境不完整，使用系统Python安装...")
                subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        else:
            print("   使用系统Python安装...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        
        print("✅ PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller安装失败: {e}")
        return False

def build_executable():
    """构建可执行文件"""
    print("🔨 开始构建可执行文件...")
    
    # 构建命令
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包成单个文件
        "--windowed",                   # Windows下不显示控制台窗口（可选）
        "--name", "xtts-api-server-mantella",  # 指定输出文件名
        "--icon", "NONE",               # 暂时不使用图标
        "--add-data", "config.ini;.",   # 包含配置文件
        "--hidden-import", "uvicorn",   # 确保包含必要的模块
        "--hidden-import", "fastapi",
        "--hidden-import", "TTS",
        "--hidden-import", "torch",
        "--hidden-import", "torchaudio",
        "--clean",                      # 清理临时文件
        "xtts_launcher.py"              # 源文件
    ]
    
    try:
        # 检查是否在虚拟环境中
        venv_path = Path(".venv")
        if venv_path.exists():
            pyinstaller_exe = venv_path / "Scripts" / "pyinstaller.exe"
            if pyinstaller_exe.exists():
                cmd[0] = str(pyinstaller_exe)
                print("   使用虚拟环境中的PyInstaller...")
        
        print(f"   执行命令: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
        print("✅ 可执行文件构建成功")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def cleanup_build_files():
    """清理构建过程中产生的临时文件"""
    print("🧹 清理临时文件...")
    
    # 要删除的文件夹
    folders_to_remove = ["build", "__pycache__"]
    files_to_remove = ["xtts-api-server-mantella.spec"]
    
    for folder in folders_to_remove:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   删除文件夹: {folder}")
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"   删除文件: {file}")
    
    print("✅ 清理完成")

def main():
    """主函数"""
    print("=" * 60)
    print("    XTTS API Server - Mantella 可执行文件构建工具")
    print("=" * 60)
    
    # 检查源文件是否存在
    if not os.path.exists("xtts_launcher.py"):
        print("❌ 未找到源文件 xtts_launcher.py")
        return
    
    # 检查PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("❌ 无法安装PyInstaller，构建失败")
            return
    
    # 构建可执行文件
    if build_executable():
        # 检查输出文件
        exe_path = Path("dist") / "xtts-api-server-mantella.exe"
        if exe_path.exists():
            print(f"🎉 构建成功！")
            print(f"📁 可执行文件位置: {exe_path.absolute()}")
            print(f"📏 文件大小: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            
            # 询问是否移动到根目录
            response = input("\n是否将exe文件移动到根目录？(y/n): ").lower().strip()
            if response in ['y', 'yes', '是']:
                target_path = Path("xtts-api-server-mantella.exe")
                if target_path.exists():
                    target_path.unlink()  # 删除已存在的文件
                shutil.move(str(exe_path), str(target_path))
                print(f"✅ 文件已移动到: {target_path.absolute()}")
        else:
            print("❌ 构建失败，未找到输出文件")
    
    # 清理临时文件
    cleanup_build_files()
    
    print("\n构建完成！")
    input("按任意键退出...")

if __name__ == "__main__":
    main()
