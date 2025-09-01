# XTTS API Server - Mantella 可执行文件构建说明

## 概述

本文档说明如何将XTTS API Server编译为独立的可执行文件 `xtts-api-server-mantella.exe`。

## 文件说明

### 核心文件
- `xtts_launcher.py` - 主启动器脚本，负责读取配置并启动API服务器
- `config.ini` - 配置文件，包含服务器启动参数
- `build_exe.bat` - 自动化构建脚本
- `build_exe_simple.py` - Python版本的构建脚本

### 生成文件
- `xtts-api-server-mantella.exe` - 最终生成的可执行文件

## 构建步骤

### 方法一：使用批处理文件（推荐）

1. **确保环境准备就绪**
   ```bash
   # 确保虚拟环境已创建并激活
   python -m venv .venv
   .venv\Scripts\activate
   
   # 安装项目依赖
   pip install -r requirements.txt
   ```

2. **运行构建脚本**
   ```bash
   # 双击运行或在命令行执行
   build_exe.bat
   ```

3. **构建过程**
   - 自动检查虚拟环境
   - 安装PyInstaller
   - 编译Python脚本为exe文件
   - 自动移动到根目录
   - 清理临时文件

### 方法二：使用Python脚本

```bash
python build_exe_simple.py
```

### 方法三：手动构建

```bash
# 安装PyInstaller
pip install pyinstaller

# 构建命令
pyinstaller --onefile --console --name "xtts-api-server-mantella" --clean xtts_launcher.py
```

## 配置文件说明

### config.ini 格式

```ini
[DEFAULT]
host = localhost
port = 8020
device = cuda
speakerfolder = speakers/
latentspeakerfolder = latent_speaker_folder/
outputfolder = output/
modelfolder = xtts_models/
modelversion = v2.0.2
listen = true
lowvram = false
deepspeed = false
```

### 配置参数说明

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| host | 服务器主机地址 | localhost | localhost, 0.0.0.0 |
| port | 服务器端口 | 8020 | 8020, 8080 |
| device | 计算设备 | cuda | cuda, cpu |
| speakerfolder | 说话人样本文件夹 | speakers/ | speakers/, voices/ |
| latentspeakerfolder | 潜在说话人文件夹 | latent_speaker_folder/ | - |
| outputfolder | 输出文件夹 | output/ | output/, generated/ |
| modelfolder | 模型文件夹 | xtts_models/ | models/, xtts_models/ |
| modelversion | 模型版本 | v2.0.2 | v2.0.2, v2.0.3, main |
| listen | 允许外部访问 | false | true, false |
| lowvram | 低显存模式 | false | true, false |
| deepspeed | DeepSpeed加速 | false | true, false |

## 使用方法

### 启动服务器

1. **使用可执行文件**
   ```bash
   # 直接双击或命令行运行
   xtts-api-server-mantella.exe
   ```

2. **配置检查**
   - 程序会自动读取 `config.ini` 文件
   - 如果配置有误会显示警告并使用默认值
   - 支持命令行参数覆盖配置文件设置

3. **访问API**
   - API文档：http://localhost:8020/docs
   - 健康检查：http://localhost:8020/health

## 故障排除

### 常见问题

1. **构建失败**
   - 确保虚拟环境正确安装
   - 检查Python版本（推荐3.11.7）
   - 确保所有依赖已安装

2. **exe文件无法运行**
   - 检查config.ini文件是否存在
   - 确保必要的文件夹存在（speakers/, output/等）
   - 检查CUDA环境（如果使用GPU）

3. **配置文件错误**
   - host参数应该是主机地址，不是端口号
   - 布尔值使用 true/false
   - 路径使用正斜杠或双反斜杠

### 调试模式

如果遇到问题，可以在命令行运行exe文件查看详细错误信息：

```bash
# 在命令行运行以查看详细输出
xtts-api-server-mantella.exe
```

## 注意事项

1. **文件大小**：生成的exe文件可能较大（100MB+），这是正常的，因为包含了所有Python依赖

2. **首次运行**：首次运行可能需要下载模型文件，请确保网络连接正常

3. **防病毒软件**：某些防病毒软件可能误报，请添加到白名单

4. **性能**：exe文件启动可能比直接运行Python脚本稍慢，这是正常现象

## 更新说明

如果需要更新：
1. 修改源代码
2. 重新运行构建脚本
3. 替换旧的exe文件

## 技术支持

如遇到问题，请检查：
- Python环境是否正确
- 依赖包是否完整安装
- 配置文件格式是否正确
- 系统资源是否充足
