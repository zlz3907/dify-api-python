# Dify API Python

Dify API Python 是一个用于与 Dify API 交互的 Python 实现。它提供了一个易于使用的接口来进行 API 调用，支持流式和非流式响应。该库还包含了一个合并流式响应的方法，使其在不支持流式响应的场景中也能方便使用。

## 安装

使用 pip 安装该包：

```bash
pip install dify-api-python
```

## 使用方法

### 导入客户端

```python
from dify_api_python import DifyClient
```

### 初始化客户端

你可以通过以下几种方式初始化 `DifyClient`：

1. 使用参数：
   ```python
   client = DifyClient(api_key='你的_api_key', base_url='https://api.dify.ai/v1')
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
API_KEY = 你的_api_key
BASE_URL = https://api.dify.ai/v1
```

注意：如果你通过参数提供 `api_key` 或 `base_url`，它们将覆盖配置文件中的值。

### 进行 API 调用

#### 聊天补全

对于聊天补全请求：

```python
response = client.chat_completion(
    query="你好，你好吗？",
    user="user123",
    inputs={},
    stream=False
)
print(response)
```

对于流式聊天补全：

```python
for chunk in client.chat_completion(
    query="给我讲个故事",
    user="user123",
    inputs={},
    stream=True
):
    print(chunk)
```

#### 文本补全

对于文本补全请求：

```python
response = client.text_completion(
    prompt="从前有座山",
    user_id="user123",
    inputs={},
    stream=False
)
print(response)
```

对于流式文本补全：

```python
for chunk in client.text_completion(
    prompt="写一首关于春天的诗",
    user_id="user123",
    inputs={},
    stream=True
):
    print(chunk)
```

#### 合并聊天补全

对于合并聊天补全（合并流式响应）：

```python
response = client.chat_completion_combined(
    query="解释量子计算",
    user="user123",
    inputs={}
)
print(response)
```

## 主要特性

- 灵活的客户端初始化（通过参数或配置文件）
- 支持流式和非流式 API 调用
- 合并流式响应的方法
- 易于使用的聊天和文本补全接口

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 许可证

本项目采用 Apache License 2.0 许可证。详见 [LICENSE](LICENSE) 文件。

## 支持

如果你遇到任何问题或有任何疑问，请在 GitHub 仓库中开一个 issue。