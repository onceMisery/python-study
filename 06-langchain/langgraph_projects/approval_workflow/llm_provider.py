from langchain.llms.base import LLM
from langchain.llms import OpenAI
import os, json

class DeepSeekLLM(LLM):
    def __init__(self, api_key, model="deepseek-chat"):
        self.api_key = api_key
        self.model = model

    @property
    def _llm_type(self):
        return "deepseek"

    def _call(self, prompt, stop=None, **kwargs):
        import requests
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        resp = requests.post(url, headers=headers, json=data)
        return resp.json()["choices"][0]["message"]["content"]

def get_llm(tenant="default"):
    config_path = os.path.join(os.path.dirname(__file__), "data", "llm_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        llm_type = config.get(tenant, "openai")
    else:
        llm_type = "openai"
    if llm_type == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY")  # 使用环境变量获取 API Key
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")
        return DeepSeekLLM(api_key=api_key)
    else:
        return OpenAI(temperature=0) 