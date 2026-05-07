# Shell 超时问题 - 快速修复

## ✅ 已完成的优化

1. ✅ 已创建优化的 `.zshrc.cursor` 配置文件
2. ✅ 已备份原始 `.zshrc` 文件

## 🚀 三种修复方案（选择一种）

### 方案 1: 在 Cursor 中增加超时（最简单，推荐）

1. 打开 Cursor 设置：`Cmd + ,` (macOS)
2. 搜索：`terminal.integrated.shellIntegration.timeout`
3. 将值改为：`30000` (30 秒)
4. 重启 Cursor

**优点**：不需要修改任何配置文件  
**缺点**：只是增加等待时间，不解决根本问题

---

### 方案 2: 禁用 oh-my-zsh 自动更新（推荐）

在你的 `~/.zshrc` 文件中，找到这些行（大约第 27-32 行）：

```bash
# zstyle ':omz:update' mode disabled  # disable automatic updates
```

**取消注释**，改为：

```bash
zstyle ':omz:update' mode disabled  # disable automatic updates
```

然后重启终端。

**优点**：解决网络调用导致的延迟  
**缺点**：需要手动更新 oh-my-zsh

---

### 方案 3: 使用优化的 .zshrc.cursor（最彻底）

1. 在 Cursor 设置中：
   - 打开：`Settings → Terminal → Integrated Shell Args`
   - 添加：`["-c", "source ~/.zshrc.cursor; exec zsh"]`

2. 或者临时替换（测试）：
   ```bash
   # 备份当前配置
   mv ~/.zshrc ~/.zshrc.original
   
   # 使用优化版本
   cp ~/.zshrc.cursor ~/.zshrc
   
   # 重启 Cursor 测试
   ```

**优点**：最快的启动速度  
**缺点**：需要维护两个配置文件

---

## 🔍 诊断结果

根据诊断，你的配置：
- ✅ 只有 1 个插件（git）- 已经很精简
- ✅ 启动时间 ~0.95 秒 - 实际上很快
- ⚠️ 可能有网络调用（oh-my-zsh 更新检查）

**建议**：先尝试**方案 1**（增加超时），如果还有问题，再使用**方案 2**（禁用自动更新）。

---

## 📝 验证修复

修复后，在 Cursor 中：
1. 关闭所有终端窗口
2. 重新打开终端
3. 应该不再出现超时错误

如果问题仍然存在，运行：
```bash
bash scripts/diagnose-shell.sh
```

查看详细诊断信息。

---

**最后更新**: 2025-12-06
