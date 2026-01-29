#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
#  圣经与资治通鉴时空宇宙观 - PDF生成脚本
# ═══════════════════════════════════════════════════════════════════════════════
#
# 用法:
#   ./scripts/generate-pdf.sh [book|academic|training|volume-N]
#
# 示例:
#   ./scripts/generate-pdf.sh              # 生成完整书稿PDF
#   ./scripts/generate-pdf.sh book         # 同上
#   ./scripts/generate-pdf.sh academic     # 生成学术资源PDF
#   ./scripts/generate-pdf.sh training     # 生成培训材料PDF
#   ./scripts/generate-pdf.sh volume-1     # 生成第1卷PDF
#
# 依赖:
#   - pandoc: brew install pandoc
#   - LaTeX:  brew install --cask mactex-no-gui (或 basictex)
# ═══════════════════════════════════════════════════════════════════════════════

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BOOK_DIR="$PROJECT_ROOT/books/bible-tongjian-parallel"
OUTPUT_DIR="$BOOK_DIR/output"
TEMPLATE_DIR="$BOOK_DIR/templates"

# 默认字体 (macOS)
MAIN_FONT="PingFang SC"
MONO_FONT="Menlo"

# 检查依赖
check_dependencies() {
    echo -e "${BLUE}检查依赖...${NC}"

    if ! command -v pandoc &> /dev/null; then
        echo -e "${RED}❌ pandoc 未安装${NC}"
        echo -e "${YELLOW}请运行: brew install pandoc${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ pandoc 已安装${NC}"

    if ! command -v xelatex &> /dev/null; then
        echo -e "${RED}❌ xelatex 未安装 (需要 LaTeX)${NC}"
        echo -e "${YELLOW}请运行: brew install --cask mactex-no-gui${NC}"
        echo -e "${YELLOW}或者:   brew install --cask basictex${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ xelatex 已安装${NC}"

    echo ""
}

# 确保输出目录存在
ensure_output_dir() {
    mkdir -p "$OUTPUT_DIR"
}

# 生成PDF
generate_pdf() {
    local input_file="$1"
    local output_file="$2"
    local title="$3"

    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}   生成PDF: $title${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""

    if [ ! -f "$input_file" ]; then
        echo -e "${RED}❌ 输入文件不存在: $input_file${NC}"
        echo -e "${YELLOW}请先运行: node scripts/build-bible-tongjian-book.js${NC}"
        exit 1
    fi

    echo -e "${BLUE}输入: $input_file${NC}"
    echo -e "${BLUE}输出: $output_file${NC}"
    echo ""

    pandoc "$input_file" \
        -o "$output_file" \
        --pdf-engine=xelatex \
        -V mainfont="$MAIN_FONT" \
        -V CJKmainfont="$MAIN_FONT" \
        -V monofont="$MONO_FONT" \
        -V geometry:margin=2.5cm \
        -V papersize=a4 \
        -V fontsize=11pt \
        -V documentclass=book \
        -V classoption=openany \
        -V linkcolor=blue \
        -V urlcolor=blue \
        -V toccolor=black \
        --toc \
        --toc-depth=3 \
        --number-sections \
        --highlight-style=tango \
        -V header-includes="\usepackage{fancyhdr}\pagestyle{fancy}\fancyhead[L]{圣经与资治通鉴时空宇宙观}" \
        2>&1 | while read line; do
            echo -e "  $line"
        done

    if [ -f "$output_file" ]; then
        echo ""
        echo -e "${GREEN}✅ PDF生成成功!${NC}"
        echo -e "${GREEN}   文件: $output_file${NC}"
        echo -e "${GREEN}   大小: $(du -h "$output_file" | cut -f1)${NC}"
        echo ""

        # 在macOS上自动打开PDF
        if [[ "$OSTYPE" == "darwin"* ]]; then
            read -p "是否打开PDF? [y/N] " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                open "$output_file"
            fi
        fi
    else
        echo -e "${RED}❌ PDF生成失败${NC}"
        exit 1
    fi
}

# 主函数
main() {
    local type="${1:-book}"

    check_dependencies
    ensure_output_dir

    case "$type" in
        book|all|"")
            # 先构建markdown
            echo -e "${BLUE}构建Markdown书稿...${NC}"
            node "$SCRIPT_DIR/build-bible-tongjian-book.js" --all

            generate_pdf \
                "$OUTPUT_DIR/bible-tongjian-complete.md" \
                "$OUTPUT_DIR/圣经与资治通鉴时空宇宙观-完整版.pdf" \
                "完整书稿"
            ;;

        academic)
            echo -e "${BLUE}构建学术资源Markdown...${NC}"
            node "$SCRIPT_DIR/build-bible-tongjian-book.js" --academic

            generate_pdf \
                "$OUTPUT_DIR/bible-tongjian-academic.md" \
                "$OUTPUT_DIR/圣经与资治通鉴-学术资源.pdf" \
                "学术资源"
            ;;

        training)
            echo -e "${BLUE}构建培训材料Markdown...${NC}"
            node "$SCRIPT_DIR/build-bible-tongjian-book.js" --training

            generate_pdf \
                "$OUTPUT_DIR/bible-tongjian-training.md" \
                "$OUTPUT_DIR/圣经与资治通鉴-培训材料.pdf" \
                "培训材料"
            ;;

        volume-*)
            vol_num="${type#volume-}"
            echo -e "${BLUE}构建第${vol_num}卷Markdown...${NC}"
            node "$SCRIPT_DIR/build-bible-tongjian-book.js" --volume "$vol_num"

            generate_pdf \
                "$OUTPUT_DIR/bible-tongjian-vol${vol_num}.md" \
                "$OUTPUT_DIR/圣经与资治通鉴-第${vol_num}卷.pdf" \
                "第${vol_num}卷"
            ;;

        revelation)
            # 啟示錄導讀
            REV_DIR="$PROJECT_ROOT/docs/study-notes-revelation"
            REV_OUTPUT="$REV_DIR/output"
            mkdir -p "$REV_OUTPUT"

            echo -e "${BLUE}构建啟示錄導讀Markdown...${NC}"
            node "$SCRIPT_DIR/build-revelation-book.js"

            echo -e "${BLUE}生成PDF...${NC}"
            pandoc "$REV_OUTPUT/revelation-complete.md" \
                -o "$REV_OUTPUT/啟示錄導讀-愛永遠長存.pdf" \
                --pdf-engine=xelatex \
                -V mainfont="$MAIN_FONT" \
                -V CJKmainfont="$MAIN_FONT" \
                -V monofont="$MONO_FONT" \
                -V geometry:margin=2.5cm \
                -V papersize=a4 \
                -V fontsize=11pt \
                -V documentclass=book \
                -V classoption=openany \
                -V linkcolor=blue \
                -V urlcolor=blue \
                -V toccolor=black \
                --toc \
                --toc-depth=3 \
                --number-sections \
                --highlight-style=tango \
                -V header-includes="\usepackage{fancyhdr}\pagestyle{fancy}\fancyhead[L]{啟示錄導讀}\fancyhead[R]{愛永遠長存}"

            if [ -f "$REV_OUTPUT/啟示錄導讀-愛永遠長存.pdf" ]; then
                echo -e "${GREEN}✅ PDF生成成功!${NC}"
                echo -e "${GREEN}   文件: $REV_OUTPUT/啟示錄導讀-愛永遠長存.pdf${NC}"
                echo -e "${GREEN}   大小: $(du -h "$REV_OUTPUT/啟示錄導讀-愛永遠長存.pdf" | cut -f1)${NC}"
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    read -p "是否打开PDF? [y/N] " -n 1 -r
                    echo
                    if [[ $REPLY =~ ^[Yy]$ ]]; then
                        open "$REV_OUTPUT/啟示錄導讀-愛永遠長存.pdf"
                    fi
                fi
            else
                echo -e "${RED}❌ PDF生成失败${NC}"
                exit 1
            fi
            ;;

        help|--help|-h)
            echo "三書出版系統 - PDF生成脚本"
            echo ""
            echo "用法:"
            echo "  ./scripts/generate-pdf.sh [类型]"
            echo ""
            echo "类型:"
            echo "  book, all     生成圣经与资治通鉴完整书稿PDF (默认)"
            echo "  academic      生成学术资源PDF"
            echo "  training      生成培训材料PDF"
            echo "  volume-N      生成第N卷PDF (N=1-8)"
            echo "  revelation    生成啟示錄導讀PDF"
            echo ""
            echo "示例:"
            echo "  ./scripts/generate-pdf.sh"
            echo "  ./scripts/generate-pdf.sh academic"
            echo "  ./scripts/generate-pdf.sh volume-1"
            echo "  ./scripts/generate-pdf.sh revelation"
            ;;

        *)
            echo -e "${RED}未知类型: $type${NC}"
            echo "运行 ./scripts/generate-pdf.sh help 查看帮助"
            exit 1
            ;;
    esac
}

main "$@"
