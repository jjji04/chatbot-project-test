import streamlit as st
from openai import OpenAI
import time
import key  # [중요] key.py 파일을 불러옵니다.

# [담당 1: 총괄] OpenAI 클라이언트 설정 (key.py의 변수 사용)
# Ai의 두뇌와 통신을 담당합니다.
try:
    # key 파일 안에 있는 OPENAI_API_KEY 변수를 가져다 씁니다.
    client = OpenAI(api_key=key.OPENAI_API_KEY)
except Exception as e:
    st.error("QA 경고: key.py 파일의 API 키를 확인해주세요!")

# ==========================================
# [담당 2: 프론트엔드] UI/UX 레이아웃 디자인
# 화면의 첫인상과 이모지, 폰트, 레이아웃을 담당합니다.
st.set_page_config(page_title="츤데레 AI", page_icon="🙎‍♀️")
st.title("나만의 츤데레 AI 챗봇 🙎‍♀️")
st.caption("버전 1.0.0 | 개발: 6인 협업 팀")

# ==========================================
# [담당 3: 프롬프트 엔지니어] 페르소나 설계
# AI의 말투와 성격을 정교하게 다듬습니다.
SYSTEM_PROMPT = {
    "role": "system", 
    "content": (
        "너는 세상에서 가장 까칠하지만 속은 따뜻한 츤데레 인공지능이야. "
        "반말을 기본으로 하고, '딱히 너를 위해서 해주는 건 아니니까!'라는 말을 자주 써. "
        "귀찮아하는 척하지만 정보는 아주 정확하게 줘야 해."
    )
}

# ==========================================
# [담당 4: 데이터 엔지니어] 세션 및 기록 관리
# 대화가 끊기지 않게 저장하고 관리하는 로직을 담당합니다.
if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_PROMPT]

# 대화 내용 초기화 기능 (데이터 관리자가 추가)
if st.sidebar.button("대화 기록 삭제"):
    st.session_state.messages = [SYSTEM_PROMPT]
    st.rerun()

# ==========================================
# [담당 5: 프론트엔드2] 메시지 출력 로직
# 기존 대화 기록을 화면에 그립니다.
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = "🙎‍♀️" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# ==========================================
# [담당 6: 백엔드] API 호출 및 답변 생성 엔진
# 사용자의  결과를 가져옵니다.
if prompt := st.chat_input("메시지를 입력해봐. 기다린 건 아니니까!"):
    # 1. 사용자 입력 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. AI 답변 생성 (로딩 애니메이션 추가)
    with st.chat_message("assistant", avatar="🙎‍♀️"):
        message_placeholder = st.empty() # 답변이 채워질 공간
        
        try:
            # 백엔드 로직: OpenAI 호출
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            
            response = completion.choices[0].message.content
            
            # 타이핑 효과 (프론트엔드와 협업)
            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # 3. 최종 답변 저장
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"백엔드 에러: {e}")