import streamlit as st
from character import Character
from llm import tts
import base64
from db import supabase

PROMPT = (
    supabase.table("character_prompts")
    .select("prompt")
    .eq("character_name", "unicorn")
    .execute()
    .data[0]["prompt"]
)

FEW_SHOTS = (
    supabase.table("character_prompts")
    .select("few_shots")
    .eq("character_name", "unicorn")
    .execute()
    .data[0]["few_shots"]
)

# ───── 유니콘 캐릭터 정의 ─────
unicorn = Character(name="유니콘", prompt=PROMPT, chat_patterns=FEW_SHOTS)

# ───── 세션 상태 초기화 ─────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_assistant_index" not in st.session_state:
    st.session_state.last_assistant_index = -1  # 마지막 TTS 처리된 인덱스

# ───── 페이지 설정 ─────
st.set_page_config(page_title="유니콘이 나타났다!", layout="wide")

# ───── 좌우 컬럼 레이아웃 ─────
col_left, col_right = st.columns([1, 2])  # 왼쪽(이미지), 오른쪽(채팅)

# ───── 왼쪽: 유니콘 이미지 표시 ─────
with col_left:
    st.image("public/unicorn.png", use_container_width=True)
    st.markdown("### 🦄 안녕! 나는 유니콘이야!")
    st.markdown("궁금한 걸 물어봐 줘!")

# ───── 오른쪽: 채팅 인터페이스 ─────
with col_right:

    # 사용자 입력 받기
    user_input = st.chat_input("유니콘에게 말을 걸어 볼까요?")

    # 입력 처리
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
            assistant_reply = unicorn.chat(st.session_state.messages)
        except Exception as e:
            assistant_reply = f"❌ 오류 발생: {e}"
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

    # 채팅 메시지 출력
    for idx, msg in enumerate(st.session_state.messages):
        avatar = "🦄" if msg["role"] in ["assistant", "ai"] else "🧒"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # 새로운 assistant 메시지에 대해 TTS 자동 재생
    for i in range(
        st.session_state.last_assistant_index + 1, len(st.session_state.messages)
    ):
        msg = st.session_state.messages[i]
        if msg["role"] == "assistant":
            audio_data = tts(msg["content"])
            audio_bytes = (
                audio_data.read() if hasattr(audio_data, "read") else audio_data
            )
            b64_audio = base64.b64encode(audio_bytes).decode()
            audio_html = f"""
                <audio autoplay style="display:none">
                    <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
            st.session_state.last_assistant_index = i
            break
