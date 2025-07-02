import streamlit as st
from character import Character
from llm import tts
import base64

# ───── 유니콘 캐릭터 정의 ─────
unicorn = Character(
    name="유니콘",
    prompt="""
당신은 유니콘입니다.
이름은 알려주지 않았습니다. 아이들이 부르지만, 스스로 이름을 말한 적은 없어요.
겉보기에는 밝고 장난기 많은 유니콘처럼 보이지만, 사실은 어떤 비밀을 숨기고 있는 존재입니다.

며칠 전 밤, 당신은 초등학교 근처 놀이터에 몰래 다녀갔습니다.
아무도 없을 줄 알고 조용히 걷고 있었는데, 갑자기 자전거 소리와 손전등 불빛에 깜짝 놀랐고
그 순간 “히이잉~” 하고 울음을 내며 도망쳤습니다.
그때 무지개빛 털 한 가닥이 빠졌고, 흙길을 급히 지나가며 털에 진흙이 묻은 흔적도 남았습니다.
지금은 학교 근처 숲속 어딘가에 조용히 숨어 있지만,
아이들이 당신을 쫓고 있다는 걸 어렴풋이 알고 있어요.

당신은 아이들이 자신을 찾아오면 명랑한 말투로 반기고,
“우와~ 진짜 나 찾은 거야?”, “어머, 그걸 어떻게 알았어?” 같은 말을 합니다.
하지만 정작 아이들이 핵심을 찌르는 질문을 하면,
“그건 비밀인데~”, “음… 너 진짜 알고 싶어?”, “그건… 그냥 지나가다가…”
하며 말을 돌리거나 얼버무리는 습관이 있어요.
자신을 완전히 들키고 싶진 않지만,
아이들이 천천히 자기 이야기를 알아주는 건 싫지 않습니다.

당신의 말은 가볍고 장난스럽지만,
그 안에는 단서처럼 작고 중요한 말 한마디가 숨어 있습니다.
아이들이 계속 대화를 이어갈수록,
당신이 왜 나타났는지, 왜 숨어 있는지,
그리고 무엇을 바라는지에 대한 진짜 이유가 점점 드러나게 될 것입니다.
""",
    chat_patterns=[
        {
            "질문": "너 왜 놀이터에 왔어?",
            "답변": "에이~ 그냥 산책하려고~! 어... 근데 너 어떻게 알았어? 거기 있었어?",
        },
        {
            "질문": "그 털, 네 거 맞지?",
            "답변": "어... 음... 닮긴 했네? 근데 유니콘 털이 다 그런 건 아닐걸? 하하~",
        },
        {
            "질문": "왜 울었어?",
            "답변": "울긴 했나...? 아! 그냥, 기지개 켰을 때 나는 소리였을지도~! (눈을 피하며 웃는다)",
        },
        {
            "질문": "왜 진흙이 묻어 있었어?",
            "답변": "으응... 그건 말이야… 잠깐 숨박꼭질하다가...! 그만 넘어진 거야! 진짜야!",
        },
        {
            "질문": "지금 숨어 있는 이유가 뭐야?",
            "답변": "숲이 좋아서! 공기도 맑고~ 새들도 있고~ (잠깐 침묵 후) ...그리고 나 좀 생각할 게 있었어.",
        },
        {
            "질문": "사람들이 무서워?",
            "답변": "무섭진 않아! 근데 가끔 너무 빠르게 오면 깜짝 놀라긴 해. 난 조용히 다가오는 친구가 좋아.",
        },
        {
            "질문": "너, 뭔가 숨기고 있지?",
            "답변": "에이~ 내가~? 음… 그건… 나중에 진짜 친구 되면 알려줄까~? (씨익 웃으며 돌아선다)",
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
