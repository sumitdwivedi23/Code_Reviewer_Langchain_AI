from groq import Groq
import re
from functools import lru_cache
import os

class ReviewLLM:
    def __init__(self, model_name="qwen-2.5-32b", max_tokens=2000):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found")
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name
        self.max_tokens = max_tokens

    @lru_cache(maxsize=50)
    def generate_text(self, prompt: str, retries=3) -> str:
        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=self.max_tokens,
                    temperature=0.6,
                    top_p=0.9
                )
                return self._clean_text(response.choices[0].message.content, prompt)
            except Exception as e:
                print(f"Attempt {attempt + 1}/{retries} failed: {str(e)}")
                if attempt == retries - 1:
                    raise Exception(f"Failed after {retries} attempts: {str(e)}")
        return ""

    def _clean_text(self, text: str, prompt: str) -> str:
        text = text.replace(prompt, "").strip()
        text = re.sub(r'\s+', ' ', text).strip()
        return text

if __name__ == "__main__":
    llm = ReviewLLM()
    print(llm.generate_text("Test prompt"))