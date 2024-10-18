import unittest
import os
import sys
from unittest.mock import patch, MagicMock
import json
import configparser

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dify_api_python.sdk import DifySDK

class TestDifySDK(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
        config.read(config_path)

        self.api_key = config.get('DEFAULT', 'API_KEY')
        self.base_url = config.get('DEFAULT', 'BASE_URL', fallback='https://api.dify.ai/v1')
        self.sdk = DifySDK(self.api_key, self.base_url)

    @patch('requests.post')
    def test_chat_message(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"answer": "Test answer"}
        mock_post.return_value = mock_response

        response = self.sdk.chat_message("Test query", "user1")
        self.assertEqual(response, {"answer": "Test answer"})

    @patch('requests.post')
    def test_completion_message(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"completion": "Test completion"}
        mock_post.return_value = mock_response

        response = self.sdk.completion_message("Test prompt", "user1")
        self.assertEqual(response, {"completion": "Test completion"})

    @patch('requests.post')
    def test_stop_chat_completion(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response

        response = self.sdk.stop_chat_completion("task1", "user1")
        self.assertEqual(response, {"result": "success"})

    @patch('requests.get')
    def Test_Get_Conversation_Messages(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"messages": ["message1", "message2"]}
        mock_get.return_value = mock_response

        response = self.sdk.get_conversation_messages("conv1", "user1")
        self.assertEqual(response, {"messages": ["message1", "message2"]})

    @patch('requests.get')
    def test_get_conversations(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"conversations": ["conv1", "conv2"]}
        mock_get.return_value = mock_response

        response = self.sdk.get_conversations("user1")
        self.assertEqual(response, {"conversations": ["conv1", "conv2"]})

    @patch('requests.delete')
    def test_delete_conversation(self, mock_delete):
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "success"}
        mock_delete.return_value = mock_response

        response = self.sdk.delete_conversation("conv1", "user1")
        self.assertEqual(response, {"result": "success"})

    @patch('requests.post')
    def test_rename_conversation(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response

        response = self.sdk.rename_conversation("conv1", "New Name", "user1")
        self.assertEqual(response, {"result": "success"})

    @patch('requests.post')
    def test_get_message_feedback(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response

        response = self.sdk.get_message_feedback("msg1", "like", "user1")
        self.assertEqual(response, {"result": "success"})

    @patch('requests.get')
    def test_get_suggested_questions(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"questions": ["Q1", "Q2"]}
        mock_get.return_value = mock_response

        response = self.sdk.get_suggested_questions("msg1", "user1")
        self.assertEqual(response, {"questions": ["Q1", "Q2"]})

    @patch('requests.post')
    def test_audio_to_text(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"text": "Transcribed text"}
        mock_post.return_value = mock_response

        response = self.sdk.audio_to_text("audio_file", "user1")
        self.assertEqual(response, {"text": "Transcribed text"})

    @patch('requests.post')
    def test_text_to_audio(self, mock_post):
        mock_response = MagicMock()
        mock_response.content = b"audio_content"
        mock_response.headers = {"Content-Type": "audio/mpeg"}
        mock_post.return_value = mock_response

        content, content_type = self.sdk.text_to_audio("Test text", user="user1")
        self.assertEqual(content, b"audio_content")
        self.assertEqual(content_type, "audio/mpeg")

    @patch('requests.get')
    def test_get_app_parameters(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"parameters": {"param1": "value1"}}
        mock_get.return_value = mock_response

        response = self.sdk.get_app_parameters("user1")
        self.assertEqual(response, {"parameters": {"param1": "value1"}})

    @patch('requests.get')
    def test_get_app_meta(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"meta": {"key": "value"}}
        mock_get.return_value = mock_response

        response = self.sdk.get_app_meta("user1")
        self.assertEqual(response, {"meta": {"key": "value"}})

    @patch('requests.post')
    def test_upload_file(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"file_id": "file1"}
        mock_post.return_value = mock_response

        response = self.sdk.upload_file("file_content", "user1")
        self.assertEqual(response, {"file_id": "file1"})

if __name__ == '__main__':
    unittest.main()
