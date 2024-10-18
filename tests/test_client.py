import unittest
import os
import sys
import json
import uuid
from unittest.mock import patch, MagicMock

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dify_api_python.client import DifyClient

class TestDifyClient(unittest.TestCase):

    def setUp(self):
        # 使用实际的配置文件
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        self.client = DifyClient(config_path=self.config_path)

    @patch('src.dify_api_python.sdk.DifySDK.chat_message')
    def test_chat_completion_combined(self, mock_chat_message):
        # 模拟 SDK 的 chat_message 方法返回
        mock_response = [
            MagicMock(data='{"event": "agent_message", "answer": "Hello", "message_id": "msg1", "created_at": 1234567890}'),
            MagicMock(data='{"event": "agent_thought", "thought": "Thinking...", "observation": "Observing...", "tool": "tool1", "tool_input": "input1"}'),
            MagicMock(data='{"event": "message_file", "type": "image", "url": "http://example.com/image.jpg"}'),
            MagicMock(data='{"event": "message_end", "conversation_id": "conv1", "metadata": {"key": "value"}}')
        ]
        mock_chat_message.return_value = mock_response

        query = "Tell me a joke"
        user = "test_user"
        response = self.client.chat_completion_combined(query, user)

        # 验证结果
        self.assertEqual(response["answer"], "Hello")
        self.assertEqual(response["conversation_id"], "conv1")
        self.assertEqual(response["message_id"], "msg1")
        self.assertEqual(response["created_at"], 1234567890)
        self.assertEqual(len(response["thoughts"]), 1)
        self.assertEqual(response["thoughts"][0]["thought"], "Thinking...")
        self.assertEqual(len(response["message_files"]), 1)
        self.assertEqual(response["message_files"][0]["type"], "image")
        self.assertEqual(response["metadata"], {"key": "value"})

        # 验证 conversation_id 是否被正确存储
        self.assertEqual(self.client.get_conversation_id(user), "conv1")

    def test_reset_conversation(self):
        user = "test_user"
        self.client.user_conversations[user] = "conv1"
        self.client.reset_conversation(user)
        self.assertIsNone(self.client.get_conversation_id(user))

    def test_get_conversation_id(self):
        user = "test_user"
        self.client.user_conversations[user] = "conv1"
        self.assertEqual(self.client.get_conversation_id(user), "conv1")

    @patch('configparser.ConfigParser.read')
    @patch('configparser.ConfigParser.get')
    def test_load_config(self, mock_get, mock_read):
        mock_get.side_effect = ["http://config.api.com/v1", "config_api_key"]
        client = DifyClient(config_path="test_config.ini")
        self.assertEqual(client.base_url, "http://config.api.com/v1")
        self.assertEqual(client.api_key, "config_api_key")

    def test_init_with_invalid_api_key(self):
        with self.assertRaises(ValueError):
            DifyClient(api_key="")

    @patch('src.dify_api_python.sdk.DifySDK')
    def test_sdk_method_call(self, mock_sdk):
        mock_sdk_instance = mock_sdk.return_value
        mock_sdk_instance.some_method.return_value = "result"
        
        self.client.sdk = mock_sdk_instance
        result = self.client.some_method()
        
        self.assertEqual(result, "result")
        mock_sdk_instance.some_method.assert_called_once()

if __name__ == '__main__':
    unittest.main()
