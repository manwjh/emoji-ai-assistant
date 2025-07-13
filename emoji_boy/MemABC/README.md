# MemABC - Memory Management System
# MemABC - 内存管理系统

## Overview / 概述

MemABC is a sophisticated memory management system designed for AI assistants, providing structured memory encoding, storage, and retrieval capabilities. The system organizes memories into three distinct categories (A, B, C) with specialized encoding and processing mechanisms.

MemABC是一个专为AI助手设计的复杂内存管理系统，提供结构化的内存编码、存储和检索功能。该系统将记忆组织成三个不同的类别（A、B、C），具有专门的编码和处理机制。

### 记忆编码模块描述
- a2b, 提取聊天对话的重要信心 -> 记忆碎片(24hr)
- a2c, 提取聊天对话的极为重要事件 -> 深层记忆（每日冥思，整理信息）
- b2c, 提取过去的信息 -> 深层记忆（冥想，很多人都会不断回顾，以保持对记忆的保持）
- dream_making, 基于b、c和模型本身知识，进行造梦，这些梦将分享给M。  

思考的过程基本都按照这个固定流程
回忆 -> MERGE_PROMPT --> MERGE_PROMPT -> 记忆更新

## Architecture / 架构

### Memory Categories / 内存类别

- **MemA**: Primary memory storage for core interactions and experiences
- **MemB**: Secondary memory for processed and categorized information  
- **MemC**: Tertiary memory for long-term storage and backup

- **MemA**: 核心交互和体验的主要内存存储
- **MemB**: 处理和分类信息的次要内存
- **MemC**: 长期存储和备份的第三级内存

### Directory Structure / 目录结构

```
MemABC/
├── a2b.sh              # Memory encoding script (A to B) / 内存编码脚本 (A到B)
├── a2c.sh              # Memory encoding script (A to C) / 内存编码脚本 (A到C)
├── encoding_a2b.py     # Python implementation of A to B encoding / A到B编码的Python实现
├── encoding_a2c.py     # Python implementation of A to C encoding / A到C编码的Python实现
├── memA/               # Primary memory storage / 主要内存存储
│   └── 20250712.txt    # Daily memory files / 每日内存文件
├── memB/               # Secondary processed memory / 次要处理内存
│   └── memB.txt        # Categorized memory data / 分类内存数据
└── memC/               # Long-term memory storage / 长期内存存储
    ├── memC.txt        # Current long-term memory / 当前长期内存
    ├── memC_back.txt   # Backup memory file / 备份内存文件
    └── memC.txt.backup # Additional backup / 额外备份
```

## Features / 功能特性

### Memory Encoding / 内存编码
- **A2B Encoding**: Converts raw memories from MemA to processed format in MemB
- **A2C Encoding**: Archives important memories to long-term storage in MemC
- **Automatic Backup**: Built-in backup mechanisms for data integrity

- **A2B编码**: 将MemA中的原始记忆转换为MemB中的处理格式
- **A2C编码**: 将重要记忆归档到MemC的长期存储中
- **自动备份**: 内置备份机制确保数据完整性

### Memory Processing / 内存处理
- Structured memory categorization / 结构化内存分类
- Temporal organization (daily files) / 时间组织（每日文件）
- Redundant storage for reliability / 冗余存储确保可靠性
- Cross-referencing capabilities / 交叉引用功能

## Usage / 使用方法

### Shell Scripts / Shell脚本

```bash
# Encode memories from A to B / 将记忆从A编码到B
./a2b.sh

# Encode memories from A to C / 将记忆从A编码到C
./a2c.sh
```

### Python Scripts / Python脚本

```python
# Import encoding modules / 导入编码模块
from encoding_a2b import encode_a2b
from encoding_a2c import encode_a2c

# Process memories / 处理记忆
encode_a2b()
encode_a2c()
```

## Memory Flow / 内存流程

1. **Input**: Raw memories stored in MemA (daily files) / **输入**: 存储在MemA中的原始记忆（每日文件）
2. **Processing**: Encoding scripts process and categorize memories / **处理**: 编码脚本处理和分类记忆
3. **Storage**: Processed memories stored in MemB and MemC / **存储**: 处理后的记忆存储在MemB和MemC中
4. **Backup**: Automatic backup creation for data safety / **备份**: 自动创建备份确保数据安全

## Configuration / 配置

The system uses configuration files to manage: / 系统使用配置文件来管理：

- Memory encoding parameters / 内存编码参数
- Storage paths and directories / 存储路径和目录
- Backup schedules and retention policies / 备份计划和保留策略
- Processing rules and categorization logic / 处理规则和分类逻辑

## Integration / 集成

MemABC integrates with the main emoji-boy AI assistant system, providing: / MemABC与主要的emoji-boy AI助手系统集成，提供：

- Persistent memory across sessions / 跨会话的持久内存
- Contextual awareness and learning / 上下文感知和学习
- Personalized interaction history / 个性化交互历史
- Adaptive behavior based on past experiences / 基于过去经验的适应性行为

## Maintenance / 维护

### Regular Tasks / 常规任务
- Monitor memory file sizes / 监控内存文件大小
- Clean up old backup files / 清理旧备份文件
- Verify data integrity / 验证数据完整性
- Update encoding parameters as needed / 根据需要更新编码参数

### Backup Strategy / 备份策略
- Automatic daily backups to memC / 自动每日备份到memC
- Manual backup creation before major updates / 重大更新前手动创建备份
- Cross-verification between backup files / 备份文件之间的交叉验证

## Development / 开发

### Adding New Memory Types / 添加新的内存类型
1. Create new memory category directory / 创建新的内存类别目录
2. Implement encoding script / 实现编码脚本
3. Update configuration files / 更新配置文件
4. Test with sample data / 使用示例数据测试

### Extending Encoding Logic / 扩展编码逻辑
1. Modify encoding Python scripts / 修改编码Python脚本
2. Update shell script wrappers / 更新shell脚本包装器
3. Add new processing rules / 添加新的处理规则
4. Validate with existing memory data / 使用现有内存数据验证

## Troubleshooting / 故障排除

### Common Issues / 常见问题
- **Memory file corruption**: Restore from backup files / **内存文件损坏**: 从备份文件恢复
- **Encoding failures**: Check file permissions and paths / **编码失败**: 检查文件权限和路径
- **Storage space**: Clean up old backup files / **存储空间**: 清理旧备份文件
- **Processing errors**: Verify input data format / **处理错误**: 验证输入数据格式

### Debug Mode / 调试模式
Enable debug logging in configuration to trace memory processing steps and identify issues. / 在配置中启用调试日志记录以跟踪内存处理步骤并识别问题。

## License / 许可证

This module is part of the emoji-ai-assistant project. See the main project LICENSE file for details. / 此模块是emoji-ai-assistant项目的一部分。详情请参阅主项目LICENSE文件。 