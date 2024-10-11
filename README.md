# Dify API Python

Dify API Python is a Python implementation for interacting with Dify's API. It provides an easy-to-use interface for making API calls, with support for both streaming and non-streaming responses. The library also includes a method to merge stream responses, making it convenient to use in scenarios where streaming is not well supported.

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

#### Chat Completion

For a chat completion request:

```python
response = client.chat_completion(
    query="Hello, how are you?",
    user="user123",
    inputs={},
    stream=False
)
print(response)
```

For a streaming chat completion:

```python
for chunk in client.chat_completion(
    query="Tell me a story",
    user="user123",
    inputs={},
    stream=True
):
    print(chunk)
```

#### Text Completion

For a text completion request:

```python
response = client.text_completion(
    prompt="Once upon a time",
    user_id="user123",
    inputs={},
    stream=False
)
print(response)
```

For a streaming text completion:

```python
for chunk in client.text_completion(
    prompt="Write a poem about",
    user_id="user123",
    inputs={},
    stream=True
):
    print(chunk)
```

#### Combined Chat Completion

For a combined chat completion (merges streaming response):

```python
response = client.chat_completion_combined(
    query="Explain quantum computing",
    user="user123",
    inputs={}
)
print(response)
```

## Key Features

- Flexible client initialization (via parameters or config file)
- Support for both streaming and non-streaming API calls
- Method to merge streaming responses
- Easy-to-use interface for chat and text completions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.