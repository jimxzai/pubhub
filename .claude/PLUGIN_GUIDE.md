# Claude Code 插件安装指南

本指南说明如何在 Claude Code 中安装和管理插件。

---

## 🚀 快速开始

### 方法 1: 使用交互式菜单（推荐）

1. 在 Claude Code 中输入：
   ```
   /plugin
   ```

2. 选择 "Browse Plugins" 浏览可用插件

3. 选择要安装的插件并确认安装

### 方法 2: 直接安装（已知插件名）

如果知道具体的插件名称和所属市场：

```
/plugin install plugin-name@marketplace-name
```

例如：
```
/plugin install github-integration@official
```

---

## 📦 添加插件市场

在安装插件之前，可能需要先添加插件市场：

```
/plugin marketplace add your-org/claude-plugins
```

将 `your-org/claude-plugins` 替换为实际的市场标识符。

---

## 🔍 浏览可用插件

### 查看所有已安装的插件

```
/plugin
```

然后选择 "Manage Plugins" 查看已安装的插件列表。

### 查看插件详情

在插件管理界面中，可以查看：
- 插件名称和版本
- 插件描述
- 新增的命令
- 插件状态（启用/禁用）

---

## ⚙️ 插件管理命令

### 启用插件

如果插件已安装但被禁用：

```
/plugin enable plugin-name@marketplace-name
```

### 禁用插件（不卸载）

临时禁用插件但保留安装：

```
/plugin disable plugin-name@marketplace-name
```

### 卸载插件

完全移除插件：

```
/plugin uninstall plugin-name@marketplace-name
```

---

## ✅ 验证安装

安装插件后：

1. **检查新命令**：
   ```
   /help
   ```
   查看是否有新命令被添加

2. **测试功能**：
   尝试使用插件提供的功能，确保正常工作

3. **查看插件列表**：
   ```
   /plugin
   ```
   然后选择 "Manage Plugins" 确认插件已安装

---

## 🎯 推荐插件（针对本项目）

### 1. GitHub 集成插件
- **用途**: 自动提交、创建 PR、同步状态
- **安装**: `/plugin install github-integration@official`

### 2. Markdown 增强插件
- **用途**: 更好的 Markdown 编辑和预览
- **安装**: `/plugin install markdown-pro@official`

### 3. 文件管理插件
- **用途**: 批量处理、文件操作
- **安装**: `/plugin install file-manager@official`

### 4. 写作助手插件
- **用途**: 文本润色、质量检查
- **安装**: `/plugin install writing-assistant@official`

---

## 🔧 故障排除

### 问题 1: 插件命令不显示

**解决方案**:
1. 确认插件已正确安装：`/plugin` → "Manage Plugins"
2. 确认插件已启用
3. 重启 Claude Code 会话

### 问题 2: 插件无法安装

**可能原因**:
- 市场未添加
- 插件名称错误
- 网络连接问题

**解决方案**:
1. 检查市场是否正确添加
2. 使用 `/plugin` 浏览可用插件，确认名称
3. 检查网络连接

### 问题 3: 插件功能不工作

**解决方案**:
1. 检查插件是否已启用
2. 查看 `/help` 确认命令是否存在
3. 查看插件文档了解正确使用方法
4. 尝试重新安装插件

---

## 📚 相关资源

- [Claude Code 官方文档](https://docs.claude.com/en/docs/claude-code/plugins)
- [插件开发指南](https://docs.claude.com/en/docs/claude-code/plugins/developing)

---

## 💡 提示

1. **定期更新插件**: 插件可能会发布新版本，定期检查更新
2. **备份配置**: 重要插件的配置建议备份
3. **测试环境**: 在重要项目中使用新插件前，先在测试环境验证
4. **社区支持**: 遇到问题可以查看插件文档或社区讨论

---

**最后更新**: 2025-12-04
**维护者**: Jim Xiao

