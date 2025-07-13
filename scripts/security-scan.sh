#!/bin/bash

# 安全扫描脚本 - 检查代码中的敏感信息

echo "🔍 开始安全扫描..."

# 颜色定义
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# 检查结果
issues_found=0

echo "📋 检查项目中的敏感信息..."

# 1. 检查硬编码的API密钥模式
echo "1. 检查硬编码的API密钥..."
if grep -r -E "(sk-[a-zA-Z0-9]{48}|sk_[a-zA-Z0-9]{48}|pk_[a-zA-Z0-9]{48})" . --exclude-dir=.git --exclude-dir=venv --exclude-dir=__pycache__ > /dev/null; then
    echo -e "${RED}❌ 发现可能的OpenAI API密钥！${NC}"
    grep -r -E "(sk-[a-zA-Z0-9]{48}|sk_[a-zA-Z0-9]{48}|pk_[a-zA-Z0-9]{48})" . --exclude-dir=.git --exclude-dir=venv --exclude-dir=__pycache__
    ((issues_found++))
else
    echo -e "${GREEN}✅ 未发现OpenAI API密钥${NC}"
fi

# 2. 检查UUID格式的字符串
echo "2. 检查UUID格式的字符串..."
uuid_matches=$(grep -r -E "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}" . --exclude-dir=.git --exclude-dir=venv --exclude-dir=__pycache__ | wc -l)
if [ $uuid_matches -gt 0 ]; then
    echo -e "${YELLOW}⚠️ 发现 $uuid_matches 个UUID格式的字符串，请确认不是API密钥：${NC}"
    grep -r -E "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}" . --exclude-dir=.git --exclude-dir=venv --exclude-dir=__pycache__
else
    echo -e "${GREEN}✅ 未发现UUID格式的字符串${NC}"
fi

# 3. 检查敏感文件
echo "3. 检查敏感文件..."
sensitive_files=$(find . -name "*.key" -o -name "*.pem" -o -name "*.p12" -o -name "*.pfx" -o -name "api_config.json" -o -name ".env" | grep -v ".git" | grep -v "venv" | wc -l)
if [ $sensitive_files -gt 0 ]; then
    echo -e "${YELLOW}⚠️ 发现 $sensitive_files 个敏感文件：${NC}"
    find . -name "*.key" -o -name "*.pem" -o -name "*.p12" -o -name "*.pfx" -o -name "api_config.json" -o -name ".env" | grep -v ".git" | grep -v "venv"
else
    echo -e "${GREEN}✅ 未发现敏感文件${NC}"
fi

# 4. 检查.gitignore配置
echo "4. 检查.gitignore配置..."
if grep -q "\.env" .gitignore && grep -q "api_config\.json" .gitignore; then
    echo -e "${GREEN}✅ .gitignore配置正确${NC}"
else
    echo -e "${RED}❌ .gitignore配置不完整，请检查${NC}"
    ((issues_found++))
fi

# 5. 检查环境变量模板
echo "5. 检查环境变量模板..."
if [ -f "emoji_boy/env_example.txt" ]; then
    if grep -q "your_.*_here" emoji_boy/env_example.txt; then
        echo -e "${GREEN}✅ 环境变量模板配置正确${NC}"
    else
        echo -e "${YELLOW}⚠️ 环境变量模板可能包含真实密钥${NC}"
        ((issues_found++))
    fi
else
    echo -e "${YELLOW}⚠️ 未找到环境变量模板文件${NC}"
fi

# 6. 检查预提交钩子
echo "6. 检查预提交钩子..."
if [ -f ".git/hooks/pre-commit" ]; then
    echo -e "${GREEN}✅ 预提交钩子已安装${NC}"
else
    echo -e "${YELLOW}⚠️ 预提交钩子未安装${NC}"
    echo "运行以下命令安装预提交钩子："
    echo "cp scripts/pre-commit-hook.sh .git/hooks/pre-commit"
fi

# 总结
echo ""
echo "📊 扫描结果总结："
if [ $issues_found -eq 0 ]; then
    echo -e "${GREEN}🎉 恭喜！未发现严重安全问题${NC}"
else
    echo -e "${RED}⚠️ 发现 $issues_found 个安全问题，请及时修复${NC}"
fi

echo ""
echo "📖 安全建议："
echo "1. 定期运行此脚本检查安全问题"
echo "2. 使用环境变量而不是硬编码密钥"
echo "3. 确保敏感文件已添加到.gitignore"
echo "4. 定期轮换API密钥"
echo "5. 参考 SECURITY.md 了解更多安全最佳实践"

exit $issues_found 