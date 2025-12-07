# Groq API 使用指南

本指南说明如何在项目中使用 Groq API 进行快速、低成本的 AI 处理。

---

## 🚀 快速开始

### 1. 安装依赖

```bash
npm install
```

这会安装 `dotenv` 包，用于加载环境变量。

### 2. 配置 API 密钥

API 密钥已保存在 `.env` 文件中（已添加到 `.gitignore`，不会提交到 Git）。

### 3. 使用 Groq Helper 脚本

```bash
# 快速分析文本
node scripts/groq-helper.js quick-analyze "你的文本内容"

# 深度分析文本
node scripts/groq-helper.js deep-analyze "你的文本内容"

# 润色文本
node scripts/groq-helper.js polish "你的文本内容"
```

---

## 📦 可用的 Groq 模型

### 快速模型（适合简单任务）
- `llama-3.1-8b-instant` - 超快速，适合简单分析和总结
- `llama-3.1-70b-versatile` - 平衡速度和性能

### 强大模型（适合复杂任务）
- `mixtral-8x7b-32768` - 长上下文，适合深度分析
- `llama-3.1-70b-versatile` - 高质量输出

---

## 💻 在代码中使用

### 基本用法

```javascript
const { callGroqAPI, quickAnalyze, deepAnalyze, polishText } = require('./scripts/groq-helper');

// 方式 1: 直接调用 API
const response = await callGroqAPI('llama-3.1-70b-versatile', '你的提示词', {
  temperature: 0.7,
  max_tokens: 2048
});

// 方式 2: 使用便捷函数
const analysis = await quickAnalyze('需要分析的文本');
const deepAnalysis = await deepAnalyze('需要深度分析的文本', '上下文信息');
const polished = await polishText('需要润色的文本', '学术但不晦涩');
```

### 在脚本中集成

```javascript
// scripts/my-script.js
require('dotenv').config();
const { quickAnalyze } = require('./groq-helper');

async function processNote(noteContent) {
  const analysis = await quickAnalyze(noteContent, '分析这篇笔记的核心观点');
  console.log('分析结果:', analysis);
  return analysis;
}
```

---

## 🎯 使用场景

### 1. 快速笔记分析
使用快速模型分析每日笔记，提取核心观点：

```bash
node scripts/groq-helper.js quick-analyze "$(cat daily-notes/drafts/2025-12-04.md)"
```

### 2. 深度内容分析
使用强大模型进行深度分析，发现跨书关联：

```bash
node scripts/groq-helper.js deep-analyze "$(cat daily-notes/published/2025-12-04.md)"
```

### 3. 文本润色
快速润色笔记，提升表达质量：

```bash
node scripts/groq-helper.js polish "$(cat daily-notes/drafts/2025-12-04.md)"
```

---

## ⚙️ API 参数说明

### `callGroqAPI(model, prompt, options)`

**参数**:
- `model` (string): 模型名称
- `prompt` (string): 提示词
- `options` (object): 可选参数
  - `temperature` (number, 0-1): 创造性，默认 0.7
  - `max_tokens` (number): 最大输出长度，默认 2048
  - `top_p` (number): 核采样，默认 1
  - `stream` (boolean): 是否流式输出，默认 false

**返回**: Promise<string> - API 响应文本

---

## 🔒 安全注意事项

1. **永远不要提交 `.env` 文件**
   - `.env` 已在 `.gitignore` 中
   - 如果意外提交，立即撤销并重新生成 API 密钥

2. **API 密钥管理**
   - 定期检查 API 使用情况
   - 设置使用限额（在 Groq 控制台）
   - 不要在代码中硬编码密钥

3. **环境变量**
   - 开发环境使用 `.env`
   - 生产环境使用系统环境变量或密钥管理服务

---

## 📊 Groq API 优势

1. **超快速度**: Groq 的硬件加速提供极快的推理速度
2. **低成本**: 相比其他 API，Groq 价格更实惠
3. **高质量模型**: 支持 Llama、Mixtral 等优秀开源模型
4. **长上下文**: 某些模型支持 32K token 上下文

---

## 🔧 故障排除

### 问题 1: "未找到 GROQ_API_KEY"

**解决方案**:
1. 确认 `.env` 文件存在
2. 确认 `.env` 文件中有 `GROQ_API_KEY=...`
3. 确认脚本中调用了 `require('dotenv').config()`

### 问题 2: API 请求失败

**可能原因**:
- API 密钥无效或过期
- 网络连接问题
- API 限额已用完

**解决方案**:
1. 检查 API 密钥是否正确
2. 检查网络连接
3. 查看 Groq 控制台的使用情况

### 问题 3: 响应速度慢

**解决方案**:
- 使用快速模型（如 `llama-3.1-8b-instant`）
- 减少 `max_tokens` 参数
- 简化提示词

---

## 📚 相关资源

- [Groq API 文档](https://console.groq.com/docs)
- [Groq 控制台](https://console.groq.com/)
- [可用模型列表](https://console.groq.com/docs/models)

---

## 💡 最佳实践

1. **选择合适的模型**
   - 简单任务用快速模型
   - 复杂任务用强大模型

2. **优化提示词**
   - 明确具体的要求
   - 提供必要的上下文
   - 使用项目中的标准格式

3. **错误处理**
   - 始终使用 try-catch
   - 记录错误日志
   - 提供降级方案

4. **成本控制**
   - 监控 API 使用量
   - 设置使用限额
   - 缓存常用结果

---

**最后更新**: 2025-12-04
**维护者**: Jim Xiao

