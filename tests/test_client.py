import unittest
import os
import sys
import json
import uuid

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

    def test_init(self):
        self.assertIsNotNone(self.client.base_url)
        self.assertIsNotNone(self.client.api_key)
        self.assertTrue(self.client.headers['Authorization'].startswith('Bearer '))

    def test_chat_completion(self):
        query = "What are the specs of the iPhone 13 Pro Max?"
        user = str(uuid.uuid4())
        inputs = {}
        files = [
            {
                "type": "image",
                "transfer_method": "remote_url",
                "url": "https://cloud.dify.ai/logo/logo-site.png"
            }
        ]
        response = self.client.chat_completion(query, user, inputs, files)
        
        print("\n--- Chat Completion Response ---")
        print(json.dumps(response, indent=2))
        
        self.assertIn('answer', response)
        self.assertIsInstance(response['answer'], str)

    def test_chat_completion_stream(self):
        query = "Tell me a short story."
        user = str(uuid.uuid4())
        inputs = {}
        files = [
            {
                "type": "image",
                "transfer_method": "remote_url",
                "url": "https://cloud.dify.ai/logo/logo-site.png"
            }
        ]
        response_stream = self.client.chat_completion(query, user, inputs, files, stream=True)
        
        print("\n--- Chat Completion Stream Response ---")
        for event in response_stream:
            print(f"Event: {event.event}")
            print(f"Data: {event.data}")
            print("---")
        
        # 不进行任何断言，只打印输出

    def test_chat_completion_combined(self):
        query = "Tell me a short story about a robot."
        user = str(uuid.uuid4())
        inputs = {}
        files = [
            {
                "type": "image",
                "transfer_method": "remote_url",
                "url": "https://cloud.dify.ai/logo/logo-site.png"
            }
        ]
        response = self.client.chat_completion_combined(query, user, inputs, files)
        
        print("\n--- Chat Completion Combined Response ---")
        print(json.dumps(response, indent=2))
        
        self.assertIn('answer', response)
        self.assertIsInstance(response['answer'], str)
        self.assertIn('conversation_id', response)  
        self.assertIn('message_id', response)
        self.assertIn('created_at', response)
        self.assertIn('thoughts', response)
        self.assertIn('message_files', response)
        self.assertIn('metadata', response)

if __name__ == '__main__':
    unittest.main()