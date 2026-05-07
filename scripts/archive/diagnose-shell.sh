#!/bin/bash

# Shell 环境诊断脚本
# 用于诊断 shell 启动缓慢问题

echo "🔍 Shell 环境诊断工具"
echo "===================="
echo ""

# 检查 shell 类型
echo "📋 Shell 信息:"
echo "  Shell: $SHELL"
echo "  Zsh 版本: $(zsh --version 2>/dev/null || echo '未安装')"
echo ""

# 检查配置文件
echo "📁 配置文件检查:"
for file in ~/.zshrc ~/.zprofile ~/.zshenv ~/.bashrc ~/.bash_profile; do
    if [ -f "$file" ]; then
        size=$(wc -l < "$file" 2>/dev/null || echo "0")
        file_size=$(du -h "$file" 2>/dev/null | cut -f1)
        echo "  ✅ $(basename $file): $size 行, $file_size"
    fi
done
echo ""

# 测试启动时间
echo "⏱️  启动时间测试:"
echo "  测试 .zshrc 加载时间..."
time zsh -i -c exit 2>&1 | grep -E "(real|user|sys)" || echo "  无法测试"
echo ""

# 检查常见慢速操作
echo "🐌 检查可能的慢速操作:"
if [ -f ~/.zshrc ]; then
    echo "  在 .zshrc 中查找:"
    grep -E "(curl|wget|brew|nvm|conda|pyenv|rbenv|update|upgrade|oh-my-zsh)" ~/.zshrc | head -10 || echo "    未发现明显慢速操作"
fi
echo ""

# 检查插件
echo "🔌 检查 oh-my-zsh 插件:"
if [ -f ~/.zshrc ] && grep -q "oh-my-zsh" ~/.zshrc; then
    plugins=$(grep -A 1 "plugins=" ~/.zshrc | grep -oE "\([^)]+\)" | tr -d '()' | tr ' ' '\n' | wc -l)
    echo "  检测到 oh-my-zsh，插件数量: $plugins"
    echo "  建议: 如果插件 > 5 个，考虑减少"
else
    echo "  未检测到 oh-my-zsh"
fi
echo ""

# 检查 PATH
echo "🛤️  PATH 检查:"
path_count=$(echo $PATH | tr ':' '\n' | wc -l | tr -d ' ')
echo "  PATH 条目数: $path_count"
if [ "$path_count" -gt 20 ]; then
    echo "  ⚠️  PATH 条目过多，可能影响启动速度"
fi
echo ""

# 检查网络相关
echo "🌐 网络相关检查:"
if [ -f ~/.zshrc ]; then
    network_calls=$(grep -cE "(curl|wget|http)" ~/.zshrc 2>/dev/null || echo "0")
    if [ "$network_calls" -gt 0 ]; then
        echo "  ⚠️  发现 $network_calls 个可能的网络调用"
        echo "  建议: 移除或延迟这些调用"
    else
        echo "  ✅ 未发现明显的网络调用"
    fi
fi
echo ""

# 总结和建议
echo "💡 建议:"
echo "  1. 如果启动时间 > 2 秒，考虑优化配置文件"
echo "  2. 移除不必要的插件和工具初始化"
echo "  3. 使用延迟加载（lazy loading）策略"
echo "  4. 查看详细指南: SHELL_TIMEOUT_FIX.md"
echo ""
