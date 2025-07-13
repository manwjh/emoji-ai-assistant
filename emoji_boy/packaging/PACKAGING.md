# Emoji Assistant 打包说明

## 打包成功！✅

### 生成的文件

打包完成后，在 `dist/` 目录下生成了以下文件：

1. **`EmojiAssistant/`** - 可执行程序目录
   - `EmojiAssistant` - 主程序可执行文件
   - `_internal/` - 程序依赖和资源文件

2. **`EmojiAssistant.app/`** - macOS 应用程序包
   - 可以直接双击运行
   - 可以拖拽到 Applications 文件夹

### 资源文件验证

✅ **emoji_boy.png** - 已正确包含  
✅ **MemABC/** - 整个目录已正确包含  
✅ **所有 Python 依赖** - 已打包到 _internal 目录

### 启动方式

#### 方式1：使用启动脚本
```bash
./launch_emoji_assistant.sh
```

#### 方式2：直接运行
```bash
./dist/EmojiAssistant/EmojiAssistant
```

#### 方式3：双击运行
- 在 Finder 中双击 `dist/EmojiAssistant.app`

### 打包命令

```bash
# 激活虚拟环境
source venv/bin/activate

# 安装打包工具
pip install pyinstaller pillow

# 执行打包
pyinstaller --onedir --windowed --name "EmojiAssistant" \
  --add-data "emoji_boy.png:." \
  --add-data "MemABC:MemABC" \
  --icon "emoji_boy.png" \
  run.py
```

### 打包参数说明

- `--onedir`: 生成目录模式（推荐 macOS）
- `--windowed`: 无控制台窗口模式
- `--name "EmojiAssistant"`: 设置程序名称
- `--add-data`: 添加资源文件
- `--icon`: 设置程序图标

### 注意事项

1. **macOS 安全限制**: 首次运行可能需要在"系统偏好设置 > 安全性与隐私"中允许运行
2. **网络权限**: 程序需要网络访问权限来调用 AI API
3. **文件权限**: 确保 MemABC 目录有读写权限

### 文件大小

- 主程序: ~1.5MB
- 总大小: ~15MB (包含所有依赖)

### 兼容性

- ✅ macOS 10.13+ (Intel/Apple Silicon)
- ✅ Python 3.7+
- ✅ 无需安装 Python 环境

### 故障排除

如果程序无法启动：

1. 检查网络连接
2. 确认 API 密钥配置
3. 查看系统日志: `Console.app`
4. 尝试在终端运行以查看错误信息

### 更新打包

如需重新打包：

```bash
# 清理旧文件
rm -rf build dist *.spec

# 重新打包
pyinstaller --onedir --windowed --name "EmojiAssistant" \
  --add-data "emoji_boy.png:." \
  --add-data "MemABC:MemABC" \
  --icon "emoji_boy.png" \
  run.py
``` 