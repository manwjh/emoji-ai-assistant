#!/bin/bash

# MemABC Initialization Script
# MemABC 初始化脚本

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 MemABC Initialization Script"
echo "=================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed or not in PATH"
    exit 1
fi

# Check if the Python script exists
if [ ! -f "init_MemABC.py" ]; then
    echo "❌ Error: init_MemABC.py not found in current directory"
    exit 1
fi

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --safe                    Safe initialization mode (creates backup before initialization)"
    echo "  --template <file_path>    Use custom system prompt template file"
    echo "  --help                    Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Normal initialization"
    echo "  $0 --safe                             # Safe initialization with backup"
    echo "  $0 --template ./custom_template.txt   # Use custom template"
    echo "  $0 --safe --template ./custom.txt     # Safe init with custom template"
    echo ""
}

# Parse command line arguments
TEMPLATE_FILE=""
SAFE_MODE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            show_usage
            exit 0
            ;;
        --safe)
            SAFE_MODE=true
            shift
            ;;
        --template)
            if [[ -n "$2" && "$2" != --* ]]; then
                TEMPLATE_FILE="$2"
                shift 2
            else
                echo "❌ Error: --template requires a file path"
                exit 1
            fi
            ;;
        *)
            echo "❌ Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate template file if provided
if [[ -n "$TEMPLATE_FILE" ]]; then
    if [[ ! -f "$TEMPLATE_FILE" ]]; then
        echo "❌ Error: Template file not found: $TEMPLATE_FILE"
        exit 1
    fi
    echo "📄 Using custom template: $TEMPLATE_FILE"
fi

# Execute initialization
if [[ "$SAFE_MODE" == true ]]; then
    echo "🛡️  Running in safe mode (will create backup first)..."
    if [[ -n "$TEMPLATE_FILE" ]]; then
        python3 init_MemABC.py --safe --template "$TEMPLATE_FILE"
    else
        python3 init_MemABC.py --safe
    fi
else
    echo "🔄 Running normal initialization..."
    if [[ -n "$TEMPLATE_FILE" ]]; then
        python3 init_MemABC.py --template "$TEMPLATE_FILE"
    else
        python3 init_MemABC.py
    fi
fi

# Check if initialization was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ MemABC initialization completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Review the created files in memA/, memB/, and memC/ directories"
    echo "   2. Run memory encoding scripts (a2b.sh, a2c.sh, b2c.sh) as needed"
    echo "   3. Use memC_to_system_prompt.sh to generate personality from deep memories"
    echo ""
    if [[ -n "$TEMPLATE_FILE" ]]; then
        echo "📄 Note: Custom template was used: $TEMPLATE_FILE"
    fi
    echo "⚠️  Note: systemprompt.txt is auto-generated. Manual edits will be overwritten."
    echo ""
else
    echo ""
    echo "❌ MemABC initialization failed!"
    echo "   Please check the error messages above and try again."
    exit 1
fi 