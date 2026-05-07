#!/bin/bash
# 构建《圣经英雄传》青少年版 PDF
# Build Bible Heroes for Teens PDF

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATE="$PROJECT_ROOT/templates/pdf/bible-heroes-teens.latex"
OUTPUT_DIR="$PROJECT_ROOT/output"
OUTPUT_FILE="$OUTPUT_DIR/bible-heroes-teens.pdf"

echo "📚 构建《圣经英雄传》青少年版..."
echo "   Building Bible Heroes for Teens..."

# 确保输出目录存在
mkdir -p "$OUTPUT_DIR"

# 创建临时工作目录
WORK_DIR=$(mktemp -d)
cp "$TEMPLATE" "$WORK_DIR/bible-heroes-teens.tex"

echo "📝 编译 LaTeX (第一遍)..."

# 第一次编译
cd "$WORK_DIR"
xelatex -interaction=nonstopmode bible-heroes-teens.tex > /dev/null 2>&1 || true

echo "📝 编译 LaTeX (第二遍)..."

# 第二次编译 (确保目录和交叉引用正确)
xelatex -interaction=nonstopmode bible-heroes-teens.tex > /dev/null 2>&1 || {
    echo "⚠️  编译有警告，查看日志..."
    cat bible-heroes-teens.log | grep -A 2 "Error\|Warning" | head -30
}

# 复制输出文件
if [ -f "bible-heroes-teens.pdf" ]; then
    cp "bible-heroes-teens.pdf" "$OUTPUT_FILE"
    echo "✅ PDF 生成成功: $OUTPUT_FILE"

    # 显示文件信息
    if command -v pdfinfo &> /dev/null; then
        echo ""
        echo "📄 PDF 信息:"
        pdfinfo "$OUTPUT_FILE" | grep -E "Pages|Page size|File size"
    fi
else
    echo "❌ PDF 生成失败"
    echo "查看错误日志:"
    cat bible-heroes-teens.log | grep -A 3 "Error" | head -20
    exit 1
fi

# 清理临时文件
rm -rf "$WORK_DIR"

echo ""
echo "🎉 完成！青少年版圣经英雄传已生成。"
echo "   Done! Bible Heroes for Teens is ready."
