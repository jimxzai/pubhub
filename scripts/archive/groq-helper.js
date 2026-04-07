#!/usr/bin/env node

/**
 * Groq API Helper Script
 * 
 * 使用 Groq API 进行文本处理、分析和生成
 * 支持快速推理和低成本处理
 */

require('dotenv').config();
const https = require('https');

const GROQ_API_KEY = process.env.GROQ_API_KEY;
const GROQ_API_URL = process.env.GROQ_API_URL || 'https://api.groq.com/openai/v1';

if (!GROQ_API_KEY) {
  console.error('❌ 错误: 未找到 GROQ_API_KEY');
  console.error('请在 .env 文件中设置 GROQ_API_KEY');
  process.exit(1);
}

/**
 * 调用 Groq API
 * @param {string} model - 模型名称 (如 'llama-3.1-70b-versatile' 或 'mixtral-8x7b-32768')
 * @param {string} prompt - 提示词
 * @param {object} options - 额外选项
 * @returns {Promise<string>} API 响应
 */
async function callGroqAPI(model, prompt, options = {}) {
  const {
    temperature = 0.7,
    max_tokens = 2048,
    top_p = 1,
    stream = false
  } = options;

  const requestData = JSON.stringify({
    model: model,
    messages: [
      {
        role: 'user',
        content: prompt
      }
    ],
    temperature,
    max_tokens,
    top_p,
    stream
  });

  return new Promise((resolve, reject) => {
    const url = new URL(`${GROQ_API_URL}/chat/completions`);
    
    const options = {
      hostname: url.hostname,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${GROQ_API_KEY}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(requestData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const response = JSON.parse(data);
            resolve(response.choices[0].message.content);
          } catch (error) {
            reject(new Error(`解析响应失败: ${error.message}`));
          }
        } else {
          reject(new Error(`API 错误 (${res.statusCode}): ${data}`));
        }
      });
    });

    req.on('error', (error) => {
      reject(new Error(`请求失败: ${error.message}`));
    });

    req.write(requestData);
    req.end();
  });
}

/**
 * 快速分析文本（使用快速模型）
 */
async function quickAnalyze(text, task = '分析') {
  const prompt = `请${task}以下文本，提供简洁、深刻的见解：

${text}

要求：
1. 提供核心观点
2. 指出关键洞察
3. 给出实用建议`;
  
  return await callGroqAPI('llama-3.1-8b-instant', prompt, {
    temperature: 0.5,
    max_tokens: 1024
  });
}

/**
 * 深度分析（使用更强大的模型）
 */
async function deepAnalyze(text, context = '') {
  const prompt = `基于以下上下文，深度分析文本：

上下文：${context || '无'}

文本：
${text}

请提供：
1. 核心主题和关键洞察
2. 与经典智慧（孙子兵法、资治通鉴、圣经）的关联
3. AI时代（2025-2035）的映射
4. 实践建议`;
  
  return await callGroqAPI('llama-3.1-70b-versatile', prompt, {
    temperature: 0.7,
    max_tokens: 2048
  });
}

/**
 * 文本润色
 */
async function polishText(text, style = '学术但不晦涩') {
  const prompt = `请润色以下文本，保持${style}的风格：

${text}

要求：
1. 保持原意不变
2. 提升表达清晰度
3. 优化语言流畅度
4. 保持中英对照（如有）`;
  
  return await callGroqAPI('mixtral-8x7b-32768', prompt, {
    temperature: 0.6,
    max_tokens: 2048
  });
}

// CLI 接口
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  const input = args.slice(1).join(' ');

  if (!command || !input) {
    console.log(`
用法:
  node scripts/groq-helper.js <command> <text>

命令:
  quick-analyze  - 快速分析文本（使用快速模型）
  deep-analyze   - 深度分析文本（使用强大模型）
  polish         - 润色文本

示例:
  node scripts/groq-helper.js quick-analyze "这是一段需要分析的文本"
  node scripts/groq-helper.js deep-analyze "这是一段需要深度分析的文本"
  node scripts/groq-helper.js polish "这是一段需要润色的文本"
    `);
    process.exit(1);
  }

  (async () => {
    try {
      let result;
      switch (command) {
        case 'quick-analyze':
          result = await quickAnalyze(input);
          break;
        case 'deep-analyze':
          result = await deepAnalyze(input);
          break;
        case 'polish':
          result = await polishText(input);
          break;
        default:
          console.error(`未知命令: ${command}`);
          process.exit(1);
      }
      console.log('\n' + result + '\n');
    } catch (error) {
      console.error('❌ 错误:', error.message);
      process.exit(1);
    }
  })();
}

// 导出供其他脚本使用
module.exports = {
  callGroqAPI,
  quickAnalyze,
  deepAnalyze,
  polishText
};

