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
        
        # 打印完整的返回结果
        print("\nFull response from chat_completion_combined:")
        for key, value in response.items():
            print(f"{key}:")
            print(json.dumps(value, indent=2))
            print()

        self.assertIn('answer', response)
        self.assertIsInstance(response['answer'], str)
        self.assertIn('conversation_id', response)  
        self.assertIn('message_id', response)
        self.assertIn('created_at', response)
        self.assertIn('thoughts', response)
        self.assertIn('message_files', response)
        self.assertIn('metadata', response)

        # 测试会话ID管理
        conversation_id = self.client.get_conversation_id(user)
        print(f"\nConversation ID for user {user}: {conversation_id}")
        self.assertIsNotNone(conversation_id)
        
        # 测试重置会话
        self.client.reset_conversation(user)
        reset_conversation_id = self.client.get_conversation_id(user)
        print(f"Conversation ID after reset: {reset_conversation_id}")
        self.assertIsNone(reset_conversation_id)

if __name__ == '__main__':
    unittest.main()
