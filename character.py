from llm import call_llm


class Character:
    def __init__(self, name: str, prompt: str, chat_patterns: list[dict[str, str]]):
        self.name = name
        self.prompt = prompt
        self.chat_patterns = chat_patterns

    def chat(self, messages: list[dict[str, str]]) -> str:
        examples = "\n".join(
            f"질문:{pattern['질문']}\n답변:{pattern['답변']}\n\n"
            for pattern in self.chat_patterns
        )
        prompt = f"""{self.prompt}
        가능하면 짧고 간결하게, 그리고 재치 있게 답변해 줘.

답변할 때 다음의 예시를 참고해 주세요.
{examples}
"""
        response = call_llm(messages=[{"role": "system", "content": prompt}] + messages)
        return response.strip()
