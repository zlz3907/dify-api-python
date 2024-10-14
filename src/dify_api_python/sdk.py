import requests
from sseclient import SSEClient

class DifySDK:
    def __init__(self, api_key, base_url='https://api.dify.ai/v1'):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def chat_message(self, query, user, inputs=None, files=None, conversation_id=None, stream=False):
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
            return SSEClient(response).events()
        else:
            response = requests.post(url, json=payload, headers=self.headers)
            return response.json()

    def completion_message(self, prompt, user, inputs=None, stream=False):
        url = f"{self.base_url}/completion-messages"
        payload = {
            "prompt": prompt,
            "user": user,
            "inputs": inputs or {}
        }

        if stream:
            response = requests.post(url, json=payload, headers=self.headers, stream=True)
            return SSEClient(response).events()
        else:
            response = requests.post(url, json=payload, headers=self.headers)
            return response.json()

    def stop_chat_completion(self, task_id, user):
        url = f"{self.base_url}/chat-messages/{task_id}/stop"
        payload = {"user": user}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def get_conversation_messages(self, conversation_id, user, first_id=None, limit=20):
        url = f"{self.base_url}/messages"
        params = {
            "conversation_id": conversation_id,
            "user": user,
            "first_id": first_id,
            "limit": limit
        }
        response = requests.get(url, params=params, headers=self.headers)
        return response.json()

    def get_conversations(self, user, last_id=None, limit=20, pinned=None):
        url = f"{self.base_url}/conversations"
        params = {
            "user": user,
            "last_id": last_id,
            "limit": limit,
            "pinned": pinned
        }
        response = requests.get(url, params=params, headers=self.headers)
        return response.json()

    def delete_conversation(self, conversation_id, user):
        url = f"{self.base_url}/conversations/{conversation_id}"
        payload = {"user": user}
        response = requests.delete(url, json=payload, headers=self.headers)
        return response.json()

    def rename_conversation(self, conversation_id, name, user, auto_generate=False):
        url = f"{self.base_url}/conversations/{conversation_id}/name"
        payload = {
            "name": name,
            "auto_generate": auto_generate,
            "user": user
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def get_message_feedback(self, message_id, rating, user):
        url = f"{self.base_url}/messages/{message_id}/feedbacks"
        payload = {
            "rating": rating,
            "user": user
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def get_suggested_questions(self, message_id, user):
        url = f"{self.base_url}/messages/{message_id}/suggested"
        params = {"user": user}
        response = requests.get(url, params=params, headers=self.headers)
        return response.json()

    def audio_to_text(self, file, user):
        url = f"{self.base_url}/audio-to-text"
        files = {"file": file}
        data = {"user": user}
        response = requests.post(url, files=files, data=data, headers=self.headers)
        return response.json()

    def text_to_audio(self, text=None, message_id=None, user=None):
        url = f"{self.base_url}/text-to-audio"
        payload = {
            "text": text,
            "message_id": message_id,
            "user": user
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.content, response.headers['Content-Type']

    def get_app_parameters(self, user):
        url = f"{self.base_url}/parameters"
        params = {"user": user}
        response = requests.get(url, params=params, headers=self.headers)
        return response.json()

    def get_app_meta(self, user):
        url = f"{self.base_url}/meta"
        params = {"user": user}
        response = requests.get(url, params=params, headers=self.headers)
        return response.json()

    def upload_file(self, file, user):
        url = f"{self.base_url}/files/upload"
        files = {"file": file}
        data = {"user": user}
        response = requests.post(url, files=files, data=data, headers=self.headers)
        return response.json()
