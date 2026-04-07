#!/bin/bash

# 创建快速启动的 .zshrc 用于 Cursor
# 这个版本禁用了可能慢速的操作

BACKUP_FILE="$HOME/.zshrc.backup.$(date +%Y%m%d_%H%M%S)"
CURSOR_ZSHRC="$HOME/.zshrc.cursor"

echo "🔧 创建优化的 .zshrc 用于 Cursor"
echo ""

# 备份当前配置
if [ -f "$HOME/.zshrc" ]; then
    cp "$HOME/.zshrc" "$BACKUP_FILE"
    echo "✅ 已备份当前 .zshrc 到: $BACKUP_FILE"
fi

# 创建优化的 .zshrc
cat > "$CURSOR_ZSHRC" << 'EOF'
# Optimized .zshrc for Cursor/IDE
# Fast startup configuration

# Disable oh-my-zsh auto-update (prevents network calls)
export ZSH="$HOME/.oh-my-zsh"
zstyle ':omz:update' mode disabled

# Disable Homebrew auto-update
export HOMEBREW_NO_AUTO_UPDATE=1

# Basic PATH
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.local/bin:$PATH"

# Load oh-my-zsh (minimal plugins)
ZSH_THEME="robbyrussell"
plugins=(git)
source $ZSH/oh-my-zsh.sh

# Basic aliases
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'

# Git configuration
export EDITOR='code'

# Optional: Add your custom paths here (but avoid slow operations)
# export PATH="$HOME/.cargo/bin:$PATH"
# export PATH="$HOME/go/bin:$PATH"
EOF

echo "✅ 已创建优化的配置: $CURSOR_ZSHRC"
echo ""
echo "📋 使用方法:"
echo "  1. 在 Cursor 设置中:"
echo "     Settings → Terminal → Integrated Shell Args"
echo "     添加: [\"-c\", \"source ~/.zshrc.cursor; exec zsh\"]"
echo ""
echo "  或者"
echo ""
echo "  2. 临时替换（测试用）:"
echo "     mv ~/.zshrc ~/.zshrc.original"
echo "     cp ~/.zshrc.cursor ~/.zshrc"
echo ""
