# Dify API Python

[English](README.md) | [中文](README_CN.md)

Dify API Python 是一个用于与 Dify API 交互的 Python 实现。它提供了一个易于使用的接口来进行 API 调用，支持流式和非流式响应。

## 安装

使用 pip 安装包：

```bash
pip install dify-api-python
```

## 使用

### 导入客户端

```python
from dify_api_python import DifyClient
```

### 初始化客户端

您可以通过几种方式初始化 `DifyClient`：

1. 使用参数：
   ```python
   client = DifyClient(api_key='your_api_key', base_url='https://api.dify.ai/v1')
   ```

2. 使用默认配置文件：
   ```python
   client = DifyClient()
   ```

3. 使用自定义配置文件：
   ```python
   client = DifyClient(config_path='/path/to/your/config.ini')
   ```

配置文件应该是 INI 格式，包含以下内容：

```ini
[DEFAULT]
API_KEY = your_api_key
BASE_URL = https://api.dify.ai/v1
```

注意：如果您提供 `api_key` 或 `base_url` 作为参数，它们将覆盖配置文件中的任何值。

### 进行 API 调用

`DifyClient` 类作为 `DifySDK` 类的包装器。SDK 中的所有方法都可以直接在客户端对象上调用。以下是可用的方法：

#### 聊天消息

```python
# 非流式
response = client.chat_message(
    query="你好，你好吗？",
    user="user123",
    inputs={},
    files=None,
    conversation_id=None,
    stream=False
)
print(response)

# 流式
for chunk in client.chat_message(
    query="讲个故事",
    user="user123",
    inputs={},
    files=None,
    conversation_id=None,
    stream=True
):
    print(chunk)
```

#### 补全消息

```python
# 非流式
response = client.completion_message(
    prompt="从前有一个",
    user="user123",
    inputs={},
    stream=False
)
print(response)

# 流式
for chunk in client.completion_message(
    prompt="写一首关于的诗",
    user="user123",
    inputs={},
    stream=True
):
    print(chunk)
```

#### 停止聊天补全

```python
result = client.stop_chat_completion(task_id, user="user123")
```

#### 获取对话消息

```python
messages = client.get_conversation_messages(conversation_id, user="user123", first_id=None, limit=20)
```

#### 获取对话列表

```python
conversations = client.get_conversations(user="user123", last_id=None, limit=20, pinned=None)
```

#### 删除对话

```python
result = client.delete_conversation(conversation_id, user="user123")
```

#### 重命名对话

```python
result = client.rename_conversation(conversation_id, name="新名称", user="user123", auto_generate=False)
```

#### 获取消息反馈

```python
feedback = client.get_message_feedback(message_id, rating, user="user123")
```

#### 获取建议问题

```python
questions = client.get_suggested_questions(message_id, user="user123")
```

#### 语音转文字

```python
with open('audio.mp3', 'rb') as audio_file:
    result = client.audio_to_text(audio_file, user="user123")
```

#### 文字转语音

```python
audio_content, content_type = client.text_to_audio(text="你好，世界！", message_id=None, user="user123")
```

#### 获取应用参数

```python
parameters = client.get_app_parameters(user="user123")
```

#### 获取应用元数据

```python
meta = client.get_app_meta(user="user123")
```

#### 上传文件

```python
with open('document.pdf', 'rb') as file:
    result = client.upload_file(file, user="user123")
```

### 额外的客户端方法

`DifyClient` 提供了一些额外的方法：

```python
# 合并聊天补全（合并流式响应）
response = client.chat_completion_combined(
    query="解释量子计算",
    user="user123",
    inputs={}
)

# 重置用户的对话
client.reset_conversation("user123")

# 获取用户的对话 ID
conversation_id = client.get_conversation_id("user123")
```

## 主要特性

- 灵活的客户端初始化（通过参数或配置文件）
- 支持流式和非流式 API 调用
- 合并流式响应的方法（`chat_completion_combined`）
- 所有 Dify API 端点的易用接口
- 对话管理
- 音频转换（文字转语音和语音转文字）
- 文件上传功能

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 许可证

本项目采用 Apache License 2.0 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 支持

如果您遇到任何问题或有疑问，请在 GitHub 仓库上开一个 issue。
