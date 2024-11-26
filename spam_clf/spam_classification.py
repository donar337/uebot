import json
import uuid
from settings import CLIENT_ID, CLIENT_SECRET
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)


class ModelReducer:
    # Инициализация модели и векторайзера
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.token_url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
        self.api_url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
        self.access_token = self._get_token()

    def _get_token(self) -> str:
        request_id = str(uuid.uuid4())
        token_data = {'scope': 'GIGACHAT_API_PERS'}
        # credentials = base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()
        token_headers = {
            'Authorization': f'Basic {self.client_secret}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': request_id
        }
        response = requests.post(self.token_url, headers=token_headers, data=token_data, verify=False)
        response.raise_for_status()
        return response.json()['access_token']

    def spam_or_not(self, s: str, temperature=0.1, max_tokens=512) -> str:
        prompt = f'Представь, что ты классификатор спама, негативных сообщений, мата и флуда. Если сообщение плохое ответь 1, если хорошее 0, от себя ничего не пиши. Если видишь мат сразу отсылай 1. Сообщение которое нужно проверить: {s}'

        payload = json.dumps({
            'model': 'GigaChat',
            'messages': [
                {
                    'role': 'user',
                    'content': f'{prompt}'
                }
            ],
            'temperature': temperature,
            'top_p': 0.1,
            'n': 1,
            'stream': False,
            'max_tokens': max_tokens,
            'repetition_penalty': 1,
            'update_interval': 0
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.post(self.api_url, headers=headers, data=payload, verify=False)
        response.raise_for_status()

        content = response.json()['choices'][0]['message']['content']
        if len(content) > 1:
            content = '1'
        return content
