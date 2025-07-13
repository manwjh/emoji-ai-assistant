#!/bin/bash

# Brain Agent 测试脚本
# 提供自动化的测试环境设置和测试执行

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BRAIN_AGENT_DIR="$PROJECT_ROOT/brain_agent"
VENV_DIR="$PROJECT_ROOT/venv"
REQUIREMENTS_FILE="$PROJECT_ROOT/requirements.txt"

# 日志函数
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_step() {
    echo -e "${CYAN}🔧 $1${NC}"
}

log_test() {
    echo -e "${PURPLE}🧪 $1${NC}"
}

# 检查Python环境
check_python() {
    log_step "检查Python环境..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        log_success "找到Python3: $(python3 --version)"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        log_success "找到Python: $(python --version)"
    else
        log_error "未找到Python环境，请先安装Python 3.7+"
        exit 1
    fi
}

# 检查虚拟环境
check_venv() {
    log_step "检查虚拟环境..."
    
    if [ -d "$VENV_DIR" ]; then
        log_success "虚拟环境已存在: $VENV_DIR"
        return 0
    else
        log_warning "虚拟环境不存在，将创建新的虚拟环境"
        return 1
    fi
}

# 创建虚拟环境
create_venv() {
    log_step "创建虚拟环境..."
    
    if [ -d "$VENV_DIR" ]; then
        log_warning "虚拟环境已存在，跳过创建"
        return 0
    fi
    
    if $PYTHON_CMD -m venv "$VENV_DIR"; then
        log_success "虚拟环境创建成功: $VENV_DIR"
    else
        log_error "虚拟环境创建失败"
        exit 1
    fi
}

# 激活虚拟环境
activate_venv() {
    log_step "激活虚拟环境..."
    
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
        log_success "虚拟环境已激活"
    elif [ -f "$VENV_DIR/Scripts/activate" ]; then
        source "$VENV_DIR/Scripts/activate"
        log_success "虚拟环境已激活"
    else
        log_error "无法找到虚拟环境激活脚本"
        exit 1
    fi
}

# 检查依赖
check_dependencies() {
    log_step "检查依赖包..."
    
    local missing_deps=()
    
    # 检查requests
    if ! python -c "import requests" 2>/dev/null; then
        missing_deps+=("requests")
    fi
    
    # 检查dotenv
    if ! python -c "import dotenv" 2>/dev/null; then
        missing_deps+=("python-dotenv")
    fi
    
    if [ ${#missing_deps[@]} -eq 0 ]; then
        log_success "所有依赖包已安装"
        return 0
    else
        log_warning "缺少依赖包: ${missing_deps[*]}"
        return 1
    fi
}

# 安装依赖
install_dependencies() {
    log_step "安装依赖包..."
    
    if [ -f "$REQUIREMENTS_FILE" ]; then
        log_info "从requirements.txt安装依赖..."
        if pip install -r "$REQUIREMENTS_FILE"; then
            log_success "依赖安装成功"
        else
            log_error "依赖安装失败"
            exit 1
        fi
    else
        log_info "安装基础依赖包..."
        if pip install requests python-dotenv; then
            log_success "基础依赖安装成功"
        else
            log_error "基础依赖安装失败"
            exit 1
        fi
    fi
}

# 检查API密钥
check_api_key() {
    log_step "检查API密钥配置..."
    
    # 检查环境变量
    if [ -n "$DOUBAO_API_KEY" ]; then
        log_success "找到环境变量DOUBAO_API_KEY"
        return 0
    fi
    
    # 检查.env文件
    if [ -f "$PROJECT_ROOT/.env" ]; then
        if grep -q "DOUBAO_API_KEY" "$PROJECT_ROOT/.env"; then
            log_success "找到.env文件中的API密钥配置"
            return 0
        fi
    fi
    
    # 检查config.py
    if [ -f "$PROJECT_ROOT/config.py" ]; then
        log_info "检查config.py中的API配置..."
        if python -c "from config import get_api_key; key = get_api_key('doubao'); print('API密钥已配置' if key and key != 'your_doubao_api_key_here' else 'API密钥未配置')" 2>/dev/null; then
            log_success "找到config.py中的API密钥配置"
            return 0
        fi
    fi
    
    log_warning "未找到API密钥配置"
    log_info "请使用以下方法之一设置API密钥:"
    log_info "1. 环境变量: export DOUBAO_API_KEY='your_api_key'"
    log_info "2. .env文件: 在项目根目录创建.env文件"
    log_info "3. 配置脚本: cd .. && python setup_api.py"
    return 1
}

# 运行测试
run_test() {
    local test_type="$1"
    
    log_test "运行$test_type测试..."
    
    cd "$BRAIN_AGENT_DIR"
    
    case "$test_type" in
        "quick")
            if python test.py --quick; then
                log_success "快速测试完成"
                return 0
            else
                log_error "快速测试失败"
                return 1
            fi
            ;;
        "interactive")
            log_info "启动交互式测试，输入 'quit' 退出"
            python test.py --interactive
            ;;
        "full")
            if python test.py --full; then
                log_success "完整测试完成"
                return 0
            else
                log_error "完整测试失败"
                return 1
            fi
            ;;
        "all")
            log_info "运行所有测试..."
            if python test.py --all; then
                log_success "所有测试完成"
                return 0
            else
                log_error "部分测试失败"
                return 1
            fi
            ;;
        "api")
            if python test.py --api-test; then
                log_success "API连接测试完成"
                return 0
            else
                log_error "API连接测试失败"
                return 1
            fi
            ;;
        "new")
            log_warning "新设计测试已被移除，请使用其他测试模式"
            return 1
            ;;
        *)
            log_error "未知的测试类型: $test_type"
            return 1
            ;;
    esac
}

# 显示帮助信息
show_help() {
    echo "Brain Agent 测试脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  quick        快速测试 (推荐) - 测试10条预定义消息"
    echo "  interactive  交互式测试 - 实时输入消息测试"
    echo "  full         完整测试 - 包含API连接和准确性测试"
    echo "  all          所有测试 - 运行快速测试和完整测试"
    echo "  api          API连接测试 - 仅测试API连接"
    echo "  new          (已移除) - 新设计测试已被移除"
    echo "  help         显示此帮助信息"
    echo ""
    echo "功能特性:"
    echo "  ✅ 自动检查Python环境"
    echo "  ✅ 自动管理虚拟环境"
    echo "  ✅ 自动安装依赖包"
    echo "  ✅ 自动检查API密钥"
    echo "  ✅ 彩色输出提示"
    echo "  ✅ 完善的错误处理"
    echo ""
    echo "示例:"
    echo "  $0 quick        # 快速测试"
    echo "  $0 interactive  # 交互式测试"
    echo "  $0 full         # 完整测试"
    echo ""
}

# 主函数
main() {
    local test_type="$1"
    
    # 显示欢迎信息
    echo -e "${CYAN}"
    echo "🧠 Brain Agent 测试脚本"
    echo "========================"
    echo -e "${NC}"
    
    # 检查参数
    if [ -z "$test_type" ] || [ "$test_type" = "help" ]; then
        show_help
        exit 0
    fi
    
    # 检查项目目录
    if [ ! -d "$BRAIN_AGENT_DIR" ]; then
        log_error "未找到brain_agent目录: $BRAIN_AGENT_DIR"
        exit 1
    fi
    
    # 环境设置
    check_python
    
    if ! check_venv; then
        create_venv
    fi
    
    activate_venv
    
    if ! check_dependencies; then
        install_dependencies
    fi
    
    # 检查API密钥（除了api测试外）
    if [ "$test_type" != "api" ]; then
        if ! check_api_key; then
            log_warning "API密钥未配置，某些测试可能失败"
        fi
    fi
    
    # 运行测试
    if run_test "$test_type"; then
        log_success "测试执行完成！"
        exit 0
    else
        log_error "测试执行失败！"
        exit 1
    fi
}

# 捕获中断信号
trap 'echo -e "\n${YELLOW}👋 测试被用户中断${NC}"; exit 1' INT

# 执行主函数
main "$@" 