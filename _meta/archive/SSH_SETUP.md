# SSH 密钥设置说明

## ✅ SSH 密钥已生成

你的 SSH 密钥已生成在：`~/.ssh/id_ed25519`

## 📋 公钥内容

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIE+HwFmVToUjAhW62IIGeIr8aRgK1kFtspssx9c1o9q4 jimxzai@users.noreply.github.com
```

## 🔧 添加到 GitHub

### 步骤 1: 复制公钥

上面的公钥内容已复制到剪贴板（如果支持），或手动复制。

### 步骤 2: 添加到 GitHub

1. 访问：https://github.com/settings/keys
2. 点击 "New SSH key" 按钮
3. 填写：
   - **Title**: `MacBook - pubhub` (或任何描述性名称)
   - **Key**: 粘贴上面的公钥内容
4. 点击 "Add SSH key"

### 步骤 3: 测试连接

```bash
ssh -T git@github.com
```

应该看到：`Hi jimxzai! You've successfully authenticated...`

### 步骤 4: 推送更改

```bash
cd /Users/jimxiao/dev/pubhub
git push origin main
```

---

## 🔄 或者使用 HTTPS（替代方案）

如果不想使用 SSH，可以切换回 HTTPS：

```bash
# 切换回 HTTPS
git remote set-url origin https://github.com/jimxzai/pubhub.git

# 使用个人访问令牌推送
# 创建令牌：https://github.com/settings/tokens
# 然后推送时使用令牌作为密码
git push origin main
```

---

## 📝 当前待推送的提交

- `a891b7c` - 📦 Add package-lock.json for dependency locking
- `46b15a9` - update

---

**提示**: 添加 SSH 密钥后，以后推送就不需要输入密码了！

