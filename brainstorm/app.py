import streamlit as st
import google.generativeai as genai
from dataclasses import dataclass
from typing import List, Set
import json

# 아이디어 데이터 클래스 정의
@dataclass
class Idea:
    content: str
    likes: int = 0
    removed: bool = False

# Gemini 모델 설정
def setup_gemini():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    return genai.GenerativeModel('gemini-1.0-pro')

# 새로운 아이디어 생성
def generate_ideas(model, topic: str, existing_ideas: List[Idea], removed_ideas: Set[str], count: int = 5) -> List[Idea]:
    # 프롬프트 구성
    prompt = f"""
    주제: {topic}
    
    다음 조건을 만족하는 창의적인 아이디어 {count}개를 생성해주세요:
    1. 각 아이디어는 구체적이고 실현 가능해야 합니다
    2. 기존 아이디어와 중복되지 않아야 합니다
    3. 제거된 아이디어와 유사하지 않아야 합니다
    
    기존 아이디어: {[idea.content for idea in existing_ideas if not idea.removed]}
    제거된 아이디어: {list(removed_ideas)}
    
    응답 형식:
    1. 첫 번째 아이디어
    2. 두 번째 아이디어
    3. 세 번째 아이디어
    ...
    """
    
    try:
        response = model.generate_content(prompt)
        # 응답 텍스트를 줄 단위로 분리하고 번호와 점을 제거
        ideas = [line.strip()[3:].strip() for line in response.text.split('\n') 
                if line.strip() and line.strip()[0].isdigit()]
        return [Idea(content=idea) for idea in ideas[:count]]
    except Exception as e:
        st.error(f"아이디어 생성 중 오류가 발생했습니다: {str(e)}")
        return []

# 세션 상태 초기화
def init_session_state():
    if 'topic' not in st.session_state:
        st.session_state.topic = ""
    if 'ideas' not in st.session_state:
        st.session_state.ideas = []
    if 'removed_ideas' not in st.session_state:
        st.session_state.removed_ideas = set()
    if 'model' not in st.session_state:
        st.session_state.model = setup_gemini()

# UI 구성
def main():
    st.set_page_config(
        page_title="AI 브레인스토밍 보드",
        page_icon="🧠",
        layout="wide"
    )
    
    # 세션 상태 초기화
    init_session_state()
    
    # 헤더 섹션
    st.title("🧠 AI 브레인스토밍 보드")
    st.markdown("""
    당신의 창의적인 아이디어를 AI와 함께 발전시켜보세요!
    원하는 주제를 입력하면 AI가 다양한 아이디어를 제안합니다.
    마음에 드는 아이디어는 좋아요를 누르고, 관련 아이디어를 더 생성할 수 있습니다.
    """)
    st.divider()
    
    # 주제 입력 섹션
    col1, col2 = st.columns([4, 1])
    with col1:
        topic = st.text_input("브레인스토밍 주제를 입력하세요", 
                            value=st.session_state.topic,
                            placeholder="예: 환경 보호를 위한 새로운 비즈니스 아이디어")
    with col2:
        if st.button("🔄 새로 시작", use_container_width=True):
            st.session_state.topic = ""
            st.session_state.ideas = []
            st.session_state.removed_ideas = set()
            st.rerun()
    
    # 주제가 변경되면 상태 업데이트
    if topic != st.session_state.topic:
        st.session_state.topic = topic
        if topic:  # 주제가 비어있지 않으면 새로운 아이디어 생성
            st.session_state.ideas = generate_ideas(
                st.session_state.model,
                topic,
                [],
                st.session_state.removed_ideas
            )
            st.rerun()
    
    # 아이디어 표시 섹션
    if st.session_state.ideas:
        st.divider()
        st.subheader("💡 생성된 아이디어")
        
        for i, idea in enumerate(st.session_state.ideas):
            if not idea.removed:
                col1, col2, col3 = st.columns([6, 1, 1])
                with col1:
                    st.write(f"**{idea.content}**")
                with col2:
                    if st.button(f"👍 {idea.likes}", key=f"like_{i}"):
                        idea.likes += 1
                with col3:
                    if st.button("❌", key=f"remove_{i}"):
                        idea.removed = True
                        st.session_state.removed_ideas.add(idea.content)
        
        # 선택된 아이디어 기반 새로운 아이디어 생성
        st.divider()
        if st.button("✨ 선택된 아이디어 기반으로 새로운 아이디어 생성"):
            liked_ideas = [idea for idea in st.session_state.ideas if idea.likes > 0 and not idea.removed]
            if liked_ideas:
                new_ideas = generate_ideas(
                    st.session_state.model,
                    st.session_state.topic,
                    liked_ideas,
                    st.session_state.removed_ideas
                )
                st.session_state.ideas.extend(new_ideas)
                st.rerun()
            else:
                st.warning("먼저 마음에 드는 아이디어에 👍를 눌러주세요!")

if __name__ == "__main__":
    main() 