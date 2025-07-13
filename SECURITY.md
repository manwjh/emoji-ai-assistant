# 🔐 安全配置指南

## API密钥安全

### ⚠️ 重要提醒
- **永远不要**将真实的API密钥提交到Git仓库
- **永远不要**在代码中硬编码API密钥
- **永远不要**在日志中输出API密钥

### 🔧 安全配置步骤

#### 1. 环境变量配置（推荐）
```bash
# 复制环境变量模板
cp emoji_boy/env_example.txt .env

# 编辑 .env 文件，填入你的真实API密钥
nano .env
```

#### 2. 使用 .env 文件
```bash
# .env 文件示例
OPENAI_API_KEY=sk-your-actual-openai-key-here
HUGGINGFACE_API_KEY=hf-your-actual-huggingface-key-here
```

#### 3. 运行时配置
如果需要在运行时配置API，请使用以下格式：
```
base_url="https://ark.cn-beijing.volces.com/api/v3"
api_key=your_actual_api_key_here
model="doubao-seed-1-6-flash-250615"
```

### 🛡️ 安全检查清单

- [ ] 确认 `.env` 文件已添加到 `.gitignore`
- [ ] 确认 `api_config.json` 已添加到 `.gitignore`
- [ ] 检查代码中没有硬编码的API密钥
- [ ] 确认日志中不会输出API密钥
- [ ] 定期轮换API密钥

### 🚨 如果发现API密钥泄露

1. **立即撤销**泄露的API密钥
2. **生成新的**API密钥
3. **更新所有**使用该密钥的地方
4. **检查Git历史**，确保没有提交敏感信息
5. **通知相关方**（如果涉及第三方服务）

### 📝 最佳实践

1. **使用环境变量**而不是配置文件
2. **使用密钥管理服务**（如AWS Secrets Manager、Azure Key Vault）
3. **定期审计**代码中的敏感信息
4. **使用预提交钩子**检查敏感信息
5. **培训团队成员**安全编码实践

### 🔍 安全扫描工具

可以使用以下工具扫描代码中的敏感信息：

```bash
# 使用 git-secrets
git secrets --install
git secrets --register-aws

# 使用 truffleHog
pip install truffleHog
truffleHog --regex --entropy=False .

# 使用 detect-secrets
pip install detect-secrets
detect-secrets scan .
``` 