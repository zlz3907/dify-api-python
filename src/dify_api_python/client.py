import configparser
import os
import json
from .sdk import DifySDK

class DifyClient:
    def __init__(self, api_key=None, base_url=None, config_path=None):
        if config_path or (not api_key and not base_url):
            self._load_config(config_path)
        
        if not hasattr(self, 'api_key') or not self.api_key:
            raise ValueError("API_KEY is not set. Please provide it as a parameter or in the configuration file.")

        self.base_url = base_url or getattr(self, 'base_url', 'https://api.dify.ai/v1')
        self.sdk = DifySDK(self.api_key, self.base_url)
        self.user_conversations = {}

    def _load_config(self, config_path=None):
        config = configparser.ConfigParser()
        
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.ini')
        
        config.read(config_path)
        
        self.base_url = config.get('DEFAULT', 'BASE_URL', fallback='https://api.dify.ai/v1')
        self.api_key = config.get('DEFAULT', 'API_KEY')

    def chat_completion_combined(self, query, user, inputs=None, files=None, conversation_id=None):
        if not conversation_id:
            conversation_id = self.user_conversations.get(user)

        response = self.sdk.chat_message(query, user, inputs, files, conversation_id, stream=True)
        combined_response = self._process_combined_response(response)
        
        # 更新或存储 conversation_id
        if combined_response["conversation_id"]:
            self.user_conversations[user] = combined_response["conversation_id"]
        
        return combined_response

    def _process_combined_response(self, response):
        combined_response = {
            "answer": "",
            "conversation_id": "",
            "message_id": "",
            "created_at": 0,
            "thoughts": [],
            "message_files": [],
            "metadata": {}
        }

        for event in response:
            data = json.loads(event.data)
            event_type = data.get("event")

            if event_type == "message_end":
                combined_response["metadata"] = data.get("metadata", {})
                combined_response["conversation_id"] = data.get("conversation_id", "")
            elif event_type == "agent_message":
                combined_response["answer"] += data.get("answer", "")
                combined_response["message_id"] = data.get("message_id", "")
                combined_response["created_at"] = data.get("created_at", 0)
            elif event_type == "agent_thought":
                combined_response["thoughts"].append({
                    "thought": data.get("thought", ""),
                    "observation": data.get("observation", ""),
                    "tool": data.get("tool", ""),
                    "tool_input": data.get("tool_input", "")
                })
            elif event_type == "message_file":
                combined_response["message_files"].append({
                    "type": data.get("type", ""),
                    "url": data.get("url", "")
                })

        return combined_response

    def __getattr__(self, name):
        return getattr(self.sdk, name)

    def reset_conversation(self, user):
        """重置指定用户的会话"""
        if user in self.user_conversations:
            del self.user_conversations[user]

    def get_conversation_id(self, user):
        """获取指定用户的会话ID"""
        return self.user_conversations.get(user)
