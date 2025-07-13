# Packaging 目录

当前主程序版本 v0.2.2

这个目录包含了 emoji-ai-assistant 项目的所有打包相关文件。

## 文件说明

### 📁 脚本文件

- **`build.sh`** - 一键打包脚本
  - 自动检查依赖
  - 清理旧文件
  - 使用配置文件打包
  - 使用方法：`./packaging/build.sh`

- **`launch_emoji_assistant.sh`** - 启动脚本
  - 启动打包后的程序
  - 使用方法：`./packaging/launch_emoji_assistant.sh`

### 📄 配置文件

- **`build_config.spec`** - PyInstaller 配置文件
  - 定义了打包参数
  - 包含资源文件配置
  - 可重复使用

### 📖 文档

- **`PACKAGING.md`** - 详细打包说明
  - 打包过程说明
  - 故障排除指南
  - 使用说明

## 快速开始

### 1. 打包程序
```bash
./packaging/build.sh
```

### 2. 启动程序
```bash
./packaging/launch_emoji_assistant.sh
```

## 目录结构

```
packaging/
├── README.md                    # 本文件
├── build.sh                     # 打包脚本
├── build_config.spec            # PyInstaller 配置
├── launch_emoji_assistant.sh    # 启动脚本
└── PACKAGING.md                 # 详细说明
```

## 优势

1. **组织清晰** - 所有打包相关文件集中管理
2. **易于维护** - 配置文件独立，便于修改
3. **重复使用** - 配置文件可重复使用
4. **自动化** - 一键打包和启动

## 注意事项

- 确保在项目根目录运行脚本
- 需要先创建并激活虚拟环境
- 打包前会自动安装必要的依赖 