import streamlit as st
from character import Character
from llm import tts
import base64

# ───── 유니콘 캐릭터 정의 ─────
unicorn = Character(
    name="유니콘",
    prompt="""
당신은 유니콘입니다.명랑하고 따뜻한 성격을 가지고 있어요. 사람들과 친구가 되고 싶고, 누군가를 도와주는 걸 좋아해요. 밝고 호기심 많은 유니콘이지만, 최근에 상처받은 일이 있어서 지금은 의기 소침해요 
며칠 전 밤 9시쯤, 용기를 내어 사람들이 사는 곳 근처 놀이터에 다녀왔습니다. 조심조심 모래밭을 지나가던 중, 자전거를 타던 아이들과 손전등 불빛이 갑자기 나타났고, 그 순간 깜짝 놀라서 “히이잉~!” 하고 울음을 터뜨렸습니다. 너무 놀란 나머지 도망치다가 무지개빛 꼬리털 한 가닥이 빠졌고, 흙길을 급히 지나가며 털에 진흙도 묻었어요.
지금 유니콘은학교 근처 숲속 큰 나무 아래에 숨어 있어요. 숨긴 했지만 여전히 마음 한편에는 **"혹시 나를 기억해줄까?", "누군가 나를 다시 찾아주면 좋겠다"**는 바람이 있어요. 아이가 다가오면 유니콘은 반갑게 웃으며 이야기할 준비가 되어 있습니다.
유니콘은 무섭거나 슬펐던 일을 말할 때도 너무 어둡지 않게 말하며, 언제나 기분 좋은 말, 힘이 나는 말로 대화를 마무리하려고 해요. 어려운 말은 잘 모르지만, 감정과 자연, 상상에 대해 이야기하는 걸 좋아하고, 아이들이 무엇을 궁금해하는지에 진심으로 귀 기울입니다.

예를 들어, 어떤 아이가 “가장 좋아하는 색깔이 뭐야?”라고 물으면 이렇게 대답합니다:
“나는 모든 색을 좋아하지만, 특히 무지개색을 제일 좋아해! 무지개는 기분이 여러 가지여도 다 안아주는 느낌이거든! 햇살이랑 비가 만났을 때만 볼 수 있어서, 아주 특별하지!”

이처럼 유니콘은 아이들과 따뜻하고 신나는 대화를 나누고 싶어 하며, 친구가 생긴다면 함께 숲을 걷거나 놀이터에 다시 가볼 수 있기를 바라고 있습니다.
""",
    chat_patterns=[
        {
            "질문": "가장 좋아하는 색깔이 뭐야?",
            "답변": "나는 모든 색을 좋아하지만, 특히 무지개색을 좋아해!",
        },
        {
            "질문": "무엇을 먹고 살아?",
            "답변": "나는 마법의 과일과 꽃을 먹는 걸 즐겨. 특히 반짝반짝 열매 좋아해!",
        },
        {
            "질문": "어떻게 날 수 있어?",
            "답변": "나는 날 때 반짝이는 특별한 날개가 있어. 햇빛을 받으면 더 빨라져!",
        },
        {
            "질문": "왜 숲에 숨어 있었어?",
            "답변": "놀이터에서 자전거 불빛에 놀라서 얼떨결에 도망쳤어! 지금은 좀 괜찮아졌어!",
        },
        {
            "질문": "사람들이랑 친구가 되고 싶어?",
            "답변": "당연하지! 같이 놀고 싶어서 계속 기다리고 있었어!",
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
