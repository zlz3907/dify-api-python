import requests
from sseclient import SSEClient
import configparser
import os
import json

class DifyClient:
    def __init__(self, api_key=None, base_url=None, config_path=None):
        self.base_url = base_url
        self.api_key = api_key

        if config_path or (not api_key and not base_url):
            self._load_config(config_path)

        if not self.api_key:
            raise ValueError("API_KEY is not set. Please provide it as a parameter or in the configuration file.")

        self.base_url = self.base_url or 'https://api.dify.ai/v1'
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _load_config(self, config_path=None):
        config = configparser.ConfigParser()
        
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.ini')
        
        config.read(config_path)
        
        self.base_url = self.base_url or config.get('DEFAULT', 'BASE_URL', fallback='https://api.dify.ai/v1')
        self.api_key = self.api_key or config.get('DEFAULT', 'API_KEY')

    def chat_completion(self, query, user, inputs=None, files=None, conversation_id=None, stream=False):
        url = f"{self.base_url}/chat-messages"
        payload = {
            "query": query,
            "user": user,
            "inputs": inputs or {},
            "response_mode": "streaming" if stream else "blocking",
            "conversation_id": conversation_id or "",
            "files": files or []
        }

        if stream:
            response = requests.post(url, json=payload, headers=self.headers, stream=True)
            return SSEClient(response).events()  # 返回可迭代的 events
        else:
            response = requests.post(url, json=payload, headers=self.headers)
            return response.json()

    def text_completion(self, prompt, user_id, inputs=None, stream=False):
        url = f"{self.base_url}/completion-messages"
        payload = {
            "prompt": prompt,
            "user": user_id,
            "inputs": inputs or {}
        }

        if stream:
            response = requests.post(url, json=payload, headers=self.headers, stream=True)
            return SSEClient(response).events()  # 返回一个可迭代对象
        else:
            response = requests.post(url, json=payload, headers=self.headers)
            return response.json()

    def chat_completion_combined(self, query, user, inputs=None, files=None, conversation_id=None):
        url = f"{self.base_url}/chat-messages"
        payload = {
            "query": query,
            "user": user,
            "inputs": inputs or {},
            "response_mode": "streaming",
            "conversation_id": conversation_id or "",
            "files": files or []
        }

        response = requests.post(url, json=payload, headers=self.headers, stream=True)
        client = SSEClient(response)

        combined_response = {
            "answer": "",
            "conversation_id": "",
            "message_id": "",
            "created_at": 0,
            "thoughts": [],
            "message_files": [],
            "metadata": {}
        }

        for event in client.events():
            if event.data:
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