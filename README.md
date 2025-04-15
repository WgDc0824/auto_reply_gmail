# Gmail 自动回复设置工具

这是一个用于设置 Gmail 自动回复（假期回复）的 Python 工具。它使用 Gmail API 来管理自动回复设置，可以设置自动回复的开启时间、结束时间、回复主题和内容。同时支持使用 OpenAI API 进行智能回复。

## 功能特点

- 设置 Gmail 自动回复功能
- 自定义自动回复的邮件主题和内容
- 设置自动回复的开始和结束时间
- 支持 HTML 格式的回复内容
- 可以选择是否只向联系人发送自动回复
- 支持使用 OpenAI API 进行智能回复
- 支持定时任务调度

## 安装要求

- Python 3.9 或更高版本
- 以下 Python 包：
  - google-api-python-client
  - google-auth-httplib2
  - google-auth-oauthlib
  - openai
  - schedule

## 安装步骤

1. 克隆或下载此仓库
2. 创建并激活虚拟环境（推荐）：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   .\venv\Scripts\activate  # Windows
   ```
3. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```
4. 在 Google Cloud Console 创建项目并启用 Gmail API
5. 下载 OAuth 2.0 客户端凭据（credentials.json）并放置在项目根目录
6. 配置 OpenAI API 密钥（可选）：
   - 创建 `api_key.env` 文件
   - 添加你的 OpenAI API 密钥

## 配置说明

1. 在 Google Cloud Console 创建项目
2. 启用 Gmail API
3. 创建 OAuth 2.0 客户端 ID
4. 下载凭据文件并重命名为 `credentials.json`
5. 将 `credentials.json` 放置在项目根目录
6. 如需使用智能回复功能，配置 OpenAI API 密钥

## 使用方法

1. 基本自动回复设置：
   ```bash
   python read_gmail.py
   ```

2. 使用智能回复功能：
   ```bash
   python auto_reply.py
   ```

3. 首次运行时会打开浏览器进行 OAuth 认证
4. 认证完成后会自动设置自动回复

## 自定义设置

在 `read_gmail.py` 或 `auto_reply.py` 文件中，你可以修改以下参数来自定义自动回复：

- `subject`: 自动回复邮件的主题
- `message`: 自动回复邮件的内容（支持 HTML 格式）
- `start_time`: 自动回复的开始时间（可选，默认为当前时间）
- `end_time`: 自动回复的结束时间（可选，默认为 24 小时后）
- OpenAI API 相关配置（如使用智能回复功能）

## 注意事项

- 首次运行需要网络连接以完成 OAuth 认证
- 确保 `credentials.json` 文件安全，不要泄露给他人
- 自动回复设置可能需要几分钟才能生效
- 建议在使用前测试自动回复功能
- 使用 OpenAI API 需要有效的 API 密钥
- 注意 API 使用限制和费用

## 许可证

MIT License

## 作者

Atomos

## 联系方式

如有问题，请联系：c08241014@gmail.com 