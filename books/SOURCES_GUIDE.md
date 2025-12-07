# 三本书公开版材料获取指南

所有材料均为公开可得或合法购买，无需依赖任何"种子项目"。

---

## 一、孙子兵法

### 中文原文（公共领域）

| 资源 | 链接 | 说明 |
|------|------|------|
| 维基文库 | https://zh.wikisource.org/wiki/孫子兵法 | 原文 + 十一家注 |
| 中国哲学书电子化计划 | https://ctext.org/art-of-war/zh | 繁体原文，可下载 |
| 国学网 | http://www.guoxue.com/zibu/sunzibf/sunzi.htm | 简体版 |

### 英文译本（公共领域 / 合法购买）

| 译者 | 年份 | 获取方式 |
|------|------|----------|
| Lionel Giles | 1910 | **免费** - [Project Gutenberg](https://www.gutenberg.org/ebooks/132) |
| Samuel B. Griffith | 1963 | 购买 - Oxford University Press |
| Ralph D. Sawyer | 1994 | 购买 - Westview Press |
| Victor Mair | 2007 | 购买 - Columbia University Press |

### 推荐下载步骤

```bash
# 1. Giles 英译（免费）
curl -o books/sunzi/sources/giles-1910.txt https://www.gutenberg.org/cache/epub/132/pg132.txt

# 2. 中文原文 - 从 ctext.org 手动复制保存
```

### 历代注疏参考

- 曹操注（最早、最权威）
- 杜牧注（唐代军事视角）
- 梅尧臣注（宋代文人视角）
- 张预注（系统性最强）

---

## 二、资治通鉴

### 中文原文

| 资源 | 链接 | 说明 |
|------|------|------|
| 中国哲学书电子化计划 | https://ctext.org/zizhi-tongjian/zh | 全294卷原文 |
| 维基文库 | https://zh.wikisource.org/wiki/資治通鑑 | 原文 |
| 国学导航 | http://www.guoxue123.com/shibu/0101/00erta/ | 胡三省注本 |

### 参考译本/白话版

| 版本 | 说明 | 获取方式 |
|------|------|----------|
| 柏杨版《柏杨版资治通鉴》 | 白话翻译，72册 | 图书馆/购买 |
| 中华书局标点本 | 学术标准版 | 购买（推荐） |

### 英文资源

**注意**：资治通鉴无完整英译本，但有部分：
- Rafe de Crespigny - 三国部分研究
- Howard Wechsler - 唐代部分研究

### 阅读策略

由于294卷太多，建议按主题阅读：
1. **兴亡节点**：秦亡、王莽、三国、安史之乱
2. **人物传**：曹操、诸葛亮、李世民等关键人物
3. **制度变迁**：官制、军制、税制

---

## 三、圣经

### 中文译本

| 版本 | 链接 | 说明 |
|------|------|------|
| 和合本（CUV） | https://www.biblegateway.com/versions/Chinese-Union-Version-Simplified-CUVS/ | 最通行 |
| 和合本修订版（RCUV） | 台湾圣经公会 | 2010年修订 |
| 新译本（CNV） | 环球圣经公会 | 现代中文 |

### 英文译本

| 版本 | 链接 | 特点 |
|------|------|------|
| ESV | https://www.esv.org/ | 严谨、学术 |
| NIV | https://www.biblegateway.com/versions/NIV/ | 易读 |
| NASB | https://www.biblegateway.com/versions/NASB/ | 最忠于原文 |
| KJV | **公共领域** - Project Gutenberg | 古典英语 |

### 免费资源

```
1. BibleGateway.com - 多版本对照
2. Bible.com (YouVersion) - App + 网页
3. Blue Letter Bible - 原文工具
4. NET Bible (netbible.org) - 带详细注释，免费
```

### 学术/考古参考

| 资源 | 说明 |
|------|------|
| NET Bible Notes | 免费的学术级注释 |
| Bible Hub | 希腊文/希伯来文对照 |
| JSTOR | 学术论文（图书馆访问） |

---

## 工具推荐

### NotebookLM 使用

1. 将上述材料整理成 PDF 或 Google Docs
2. 上传到 NotebookLM
3. 生成 Audio Overview

### 本地管理

```
推荐：Obsidian
- 免费，离线
- 支持双向链接
- 可视化关系图
```

---

## 下载脚本示例

```bash
#!/bin/bash
# download-sources.sh

# 孙子兵法 - Giles 英译
mkdir -p books/sunzi/sources
curl -o books/sunzi/sources/giles-1910.txt \
  https://www.gutenberg.org/cache/epub/132/pg132.txt

# KJV 圣经（公共领域）
mkdir -p books/bible/sources
curl -o books/bible/sources/kjv.txt \
  https://www.gutenberg.org/cache/epub/10/pg10.txt

echo "下载完成！"
echo "注意：中文材料需要手动从 ctext.org 复制保存"
```

---

## 版权说明

| 材料 | 版权状态 |
|------|----------|
| 孙子兵法原文 | 公共领域（2500年前） |
| Giles 英译 | 公共领域（1910年） |
| 资治通鉴原文 | 公共领域（1000年前） |
| 柏杨白话版 | 有版权，仅供参考 |
| KJV 圣经 | 公共领域（1611年） |
| ESV/NIV/NASB | 有版权，可个人使用 |
| 和合本 | 公共领域 |

**原则**：优先使用公共领域材料，有版权材料仅供学习参考。
