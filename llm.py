import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()


class Qwen:
    def __init__(self, max_tokens=256, temperature=0.0, top_k=1):
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_k = top_k
        self.model = os.getenv("QWEN_MODEL")
        hostname = os.getenv("QWEN_HOSTNAME")
        self.client = OpenAI(
            base_url=f"{hostname}:8000/v1",
            api_key=os.getenv("QWEN_API_KEY"),
        )

    def _query(self, query):
        kwargs = {
            "model": self.model,
            "messages": [{"role": "user", "content": query}],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        if self.top_k != -1:
            kwargs["extra_body"] = {"top_k": self.top_k}
        resp = self.client.chat.completions.create(**kwargs)
        return resp.choices[0].message.content

    def chat(self, queries):
        if isinstance(queries, str):
            return self._query(queries)
        elif isinstance(queries, list):
            results = [None] * len(queries)
            with ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(self._query, q): i for i, q in enumerate(queries)
                }
                for future in as_completed(futures):
                    results[futures[future]] = future.result()
            return results
