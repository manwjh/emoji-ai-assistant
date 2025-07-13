#!/bin/bash

# 预提交钩子脚本 - 检查敏感信息

echo "🔍 检查代码中的敏感信息..."

# 检查是否包含真实的API密钥模式
if git diff --cached | grep -E "(sk-[a-zA-Z0-9]{48}|sk_[a-zA-Z0-9]{48}|pk_[a-zA-Z0-9]{48})" > /dev/null; then
    echo "❌ 检测到可能的OpenAI API密钥！"
    echo "请检查你的代码，确保没有提交真实的API密钥。"
    exit 1
fi

# 检查是否包含UUID格式的API密钥
if git diff --cached | grep -E "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}" > /dev/null; then
    echo "⚠️ 检测到UUID格式的字符串，请确认不是API密钥："
    git diff --cached | grep -E "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    echo "如果确认不是敏感信息，请继续提交。"
fi

# 检查是否包含常见的敏感文件
if git diff --cached --name-only | grep -E "\.(key|pem|p12|pfx)$" > /dev/null; then
    echo "❌ 检测到密钥文件！"
    echo "请确认这些文件不应该被提交到仓库。"
    exit 1
fi

# 检查是否包含配置文件
if git diff --cached --name-only | grep -E "(api_config\.json|config\.json|secrets\.json)" > /dev/null; then
    echo "⚠️ 检测到配置文件，请确认不包含敏感信息："
    git diff --cached --name-only | grep -E "(api_config\.json|config\.json|secrets\.json)"
fi

echo "✅ 安全检查通过"
exit 0 