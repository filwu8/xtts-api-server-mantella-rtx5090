# XTTS API Server - Mantella 使用指南

## 🎉 构建成功！

您的 `xtts-api-server-mantella.exe` 可执行文件已成功创建并测试通过！

## 📁 文件信息

- **文件名**: `xtts-api-server-mantella.exe`
- **文件大小**: 约 6.9 MB
- **位置**: 项目根目录
- **状态**: ✅ 已测试，运行正常

## 🚀 启动方式

### 方法一：双击启动（推荐）
直接双击 `xtts-api-server-mantella.exe` 文件即可启动

### 方法二：命令行启动
```bash
# 在项目根目录下执行
.\xtts-api-server-mantella.exe
```

## 📋 配置说明

程序会自动读取 `config.ini` 文件中的配置：

```ini
[DEFAULT]
host = localhost          # 主机地址（注意：您的配置中8280有误，程序会自动修正）
port = 8020              # 端口号
device = cpu             # 计算设备（cpu/cuda）
speakerfolder = speakers/
latentspeakerfolder = latent_speaker_folder/
outputfolder = output/
modelfolder = xtts_models/
modelversion = v2.0.2
listen = true            # 允许外部访问
lowvram = false          # 低显存模式
deepspeed = false        # DeepSpeed加速
```

## 🔧 启动过程

程序启动时会显示以下信息：

1. **环境检查** - 检查Python环境和虚拟环境
2. **配置加载** - 读取config.ini文件
3. **参数构建** - 根据配置构建启动参数
4. **模型加载** - 加载XTTS模型（首次启动较慢）
5. **说话人处理** - 处理说话人样本和潜在向量
6. **服务器启动** - 启动FastAPI服务器

## 🌐 访问API

启动成功后，您可以通过以下方式访问：

- **API文档**: http://localhost:8020/docs
- **健康检查**: http://localhost:8020/health
- **基础URL**: http://localhost:8020

## 📊 运行状态

从测试结果可以看到：

- ✅ 模型加载成功（v2.0.2）
- ✅ 加载了281个预存的潜在向量
- ✅ 为20个新的说话人创建了潜在向量
- ✅ 服务器在端口8020上运行
- ✅ 支持多语言（英语、日语、中文等）

## 🎯 主要功能

1. **文本转语音** - 将文本转换为语音
2. **声音克隆** - 使用说话人样本进行声音克隆
3. **多语言支持** - 支持多种语言的语音合成
4. **API接口** - 提供RESTful API接口
5. **Mantella集成** - 专为Mantella优化

## 🛑 停止服务器

- 在控制台窗口中按 `Ctrl+C`
- 或直接关闭控制台窗口

## ⚠️ 注意事项

1. **首次启动** - 首次启动会下载模型文件，需要网络连接
2. **配置修正** - 程序检测到config.ini中host配置错误（8280），已自动修正为localhost
3. **资源占用** - 模型加载会占用一定的内存和CPU资源
4. **防火墙** - 如果启用了外部访问，可能需要配置防火墙规则

## 🔧 故障排除

### 常见问题

1. **启动失败**
   - 检查config.ini文件是否存在
   - 确保必要的文件夹存在（speakers/, output/等）
   - 检查网络连接（首次启动需要下载模型）

2. **模型加载失败**
   - 检查网络连接
   - 确保有足够的磁盘空间
   - 检查xtts_models/文件夹权限

3. **API无法访问**
   - 检查端口8020是否被占用
   - 确认防火墙设置
   - 检查服务器是否正常启动

### 调试模式

如果遇到问题，可以在命令行运行exe文件查看详细日志：

```bash
.\xtts-api-server-mantella.exe
```

## 📈 性能优化建议

1. **使用GPU** - 将config.ini中的device改为cuda（如果有NVIDIA显卡）
2. **启用DeepSpeed** - 设置deepspeed = true（需要兼容的GPU）
3. **低显存模式** - 如果显存不足，设置lowvram = true

## 🔄 更新说明

如果需要更新程序：
1. 修改源代码
2. 重新运行构建脚本
3. 替换旧的exe文件

## 📞 技术支持

如果遇到问题，请检查：
- 配置文件格式是否正确
- 系统资源是否充足
- 网络连接是否正常
- 相关文件夹是否存在

---

**恭喜！您的XTTS API Server已成功部署并可以正常使用！** 🎉
