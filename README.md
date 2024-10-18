# Dify API Python

[English](README.md) | [中文](README_CN.md)

Dify API Python is a Python implementation for interacting with Dify's API. It provides an easy-to-use interface for making API calls, with support for both streaming and non-streaming responses.

## Installation

Install the package using pip:

```bash
pip install dify-api-python
```

## Usage

### Importing the Client

```python
from dify_api_python import DifyClient
```

### Initializing the Client

You can initialize the `DifyClient` in several ways:

1. Using parameters:
   ```python
   client = DifyClient(api_key='your_api_key', base_url='https://api.dify.ai/v1')
   ```

2. Using a default configuration file:
   ```python
   client = DifyClient()
   ```

3. Using a custom configuration file:
   ```python
   client = DifyClient(config_path='/path/to/your/config.ini')
   ```

The configuration file should be in INI format and include the following:

```ini
[DEFAULT]
API_KEY = your_api_key
BASE_URL = https://api.dify.ai/v1
```

Note: If you provide `api_key` or `base_url` as parameters, they will override any values in the configuration file.

### Making API Calls

The `DifyClient` class acts as a wrapper for the `DifySDK` class. All methods available in the SDK can be called directly on the client object. Here are the available methods:

#### Chat Message

```python
# Non-streaming
response = client.chat_message(
    query="Hello, how are you?",
    user="user123",
    inputs={},
    files=None,
    conversation_id=None,
    stream=False
)
print(response)

# Streaming
for chunk in client.chat_message(
    query="Tell me a story",
    user="user123",
    inputs={},
    files=None,
    conversation_id=None,
    stream=True
):
print(chunk)
```

#### Completion Message

```python
# Non-streaming
response = client.completion_message(
    prompt="Once upon a time",
    user="user123",
    inputs={},
    stream=False
)
print(response)

# Streaming
for chunk in client.completion_message(
    prompt="Write a poem about",
    user="user123",
    inputs={},
    stream=True
):
    print(chunk)
```

#### Stop Chat Completion

```python
result = client.stop_chat_completion(task_id, user="user123")
```

#### Get Conversation Messages

```python
messages = client.get_conversation_messages(conversation_id, user="user123", first_id=None, limit=20)
```

#### Get Conversations

```python
conversations = client.get_conversations(user="user123", last_id=None, limit=20, pinned=None)
```

#### Delete Conversation

```python
result = client.delete_conversation(conversation_id, user="user123")
```

#### Rename Conversation

```python
result = client.rename_conversation(conversation_id, name="New Name", user="user123", auto_generate=False)
```

#### Get Message Feedback

```python
feedback = client.get_message_feedback(message_id, rating, user="user123")
```

#### Get Suggested Questions

```python
questions = client.get_suggested_questions(message_id, user="user123")
```

#### Audio to Text

```python
with open('audio.mp3', 'rb') as audio_file:
    result = client.audio_to_text(audio_file, user="user123")
```

#### Text to Audio

```python
audio_content, content_type = client.text_to_audio(text="Hello, world!", message_id=None, user="user123")
```

#### Get App Parameters

```python
parameters = client.get_app_parameters(user="user123")
```

#### Get App Meta

```python
meta = client.get_app_meta(user="user123")
```

#### Upload File

```python
with open('document.pdf', 'rb') as file:
    result = client.upload_file(file, user="user123")
```

### Additional Client Methods

The `DifyClient` provides some additional methods:

```python
# Combined chat completion (merges streaming response)
response = client.chat_completion_combined(
    query="Explain quantum computing",
    user="user123",
    inputs={}
)

# Reset a user's conversation
client.reset_conversation("user123")

# Get a user's conversation ID
conversation_id = client.get_conversation_id("user123")
```

## Key Features

- Flexible client initialization (via parameters or config file)
- Support for both streaming and non-streaming API calls
- Method to merge streaming responses (`chat_completion_combined`)
- Easy-to-use interface for all Dify API endpoints
- Conversation management
- Audio conversion (text-to-speech and speech-to-text)
- File upload functionality

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
