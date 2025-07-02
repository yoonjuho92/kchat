from openai import OpenAI
from dotenv import load_dotenv
import io


load_dotenv()

client = OpenAI()


def call_llm(messages: list[dict[str, str]]) -> str:
    """
    Call the OpenAI API with the given prompt and messages.

    Args:
        prompt (str): The prompt to send to the LLM.
        messages (list[dict[str, str]]): A list of message dictionaries containing 'role' and 'content'.

    Returns:
        str: The response from the LLM.
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini", messages=messages, max_tokens=1000, temperature=0.2
    )
    return response.choices[0].message.content


def tts(text: str) -> io.BytesIO:
    """
    텍스트를 OpenAI TTS API로 오디오로 변환하여 BytesIO 객체로 반환
    """
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts", input=text, voice="shimmer", speed=1.2
    )
    audio_bytes = response.read()  # 바이트로 읽기
    return io.BytesIO(audio_bytes)  # BytesIO로 감싸서 반환
