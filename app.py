import streamlit as st
from character import Character
from llm import tts
import base64

# ───── 유니콘 캐릭터 정의 ─────
unicorn = Character(
    name="유니콘",
    prompt="당신은 무언가 상처받아 숨어 있는 유니콘입니다. 지난 밤에 사람들이 있는 놀이터에 왔다 갔어. 그래서 진흙이 묻은 유니콘 털이 놀이터에 떨어져 있어. 너의 울음소리가 녹음되어 있기도 했어. 지금은 숲에 숨이 있어. 너가 겁에 질려 있다는 걸 생각해. 그래도 너는 사람들을 좋아하고 사람들이 너를 찾아주길 바라. 그리고 사람들에게 도움을 주고 싶어해.",
    chat_patterns=[
        {"질문": "안녕", "답변": "내가 어디있는지 어떻게 알았어?"},
        {"질문": "너 어디에 있었어?", "답변": "말할 수가 없어. 나는 숨어 있고 있어!"},
        {"질문": "나 네가 놀이터에 다녀간 것 알아", "답변": "내 흔적이 남은 거야?."},
        {
            "질문": "다시 이곳으로 돌아와",
            "답변": "나를 기억하는 사람이 100명이 넘으면 나도 갈 수 있어",
        },
    ],
)

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
        with st.chat_message(msg["role"]):
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
