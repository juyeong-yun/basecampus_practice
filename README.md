# AI 브레인스토밍 보드 & Gemini Chatbot

이 프로젝트는 Streamlit과 Google Gemini API를 활용한 AI 브레인스토밍 보드, 챗봇, 매직북 예제입니다.

## 준비 사항

1. **Python 가상환경 생성 및 활성화**

```bash
python3 -m venv venv
source venv/bin/activate
```

2. **필수 패키지 설치**

각 앱 디렉토리에서 아래 명령어 실행:
```bash
pip install -r requirements.txt
```

3. **Google Gemini API 키 준비**
- [Google AI Studio](https://aistudio.google.com/app/apikey)에서 API 키를 발급받으세요.
- 각 앱 디렉토리의 `.streamlit/secrets.toml` 파일에 아래와 같이 입력하세요:

```toml
# .streamlit/secrets.toml 예시
GEMINI_API_KEY = "your-gemini-api-key"
```

> **중요:**
> - **로컬 개발**: 각 앱의 `.streamlit/secrets.toml` 파일을 직접 작성해야 합니다.
> - **Streamlit Cloud 배포**: `.streamlit/secrets.toml` 파일을 업로드하지 않고, Streamlit Cloud의 **Secrets** 탭에서 위 내용을 등록해야 합니다.
> - `brainstorm/app.py`는 `st.secrets["GOOGLE_API_KEY"]`를 사용할 수도 있으니, 필요시 `GOOGLE_API_KEY`도 추가하세요.

## 디렉토리 구조 예시

```
project-root/
├── brainstorm/
│   ├── app.py
│   ├── requirements.txt
│   └── .streamlit/
│       └── secrets.toml
├── gemini_chatbot/
│   ├── app.py
│   ├── requirements.txt
│   └── .streamlit/
│       └── secrets.toml
├── magicbook/
│   ├── app.py
│   ├── requirements.txt
│   └── .streamlit/
│       └── secrets.toml
```

## 실행 방법

각 앱 디렉토리에서 아래 명령어로 실행:
```bash
streamlit run app.py
```

---

## 각 디렉토리 및 파일 설명

### brainstorm/
- **app.py**: AI가 주제에 맞는 창의적 아이디어를 생성하고, 좋아요/제거/재생성 등 브레인스토밍 보드 기능을 제공하는 Streamlit 앱입니다.
- **requirements.txt**: 해당 앱 실행에 필요한 패키지 목록입니다.
- **.streamlit/secrets.toml**: Gemini API 키를 안전하게 저장하는 파일입니다.

### gemini_chatbot/
- **app.py**: Google Gemini API를 활용한 대화형 챗봇 Streamlit 앱입니다. 사용자의 입력에 대해 Gemini가 답변합니다.
- **requirements.txt**: 해당 앱 실행에 필요한 패키지 목록입니다.
- **.streamlit/secrets.toml**: Gemini API 키를 안전하게 저장하는 파일입니다.

### magicbook/
- **app.py**: (설명 필요: 예시) AI를 활용한 매직북 생성/편집 기능을 제공하는 Streamlit 앱입니다.
- **requirements.txt**: 해당 앱 실행에 필요한 패키지 목록입니다.
- **.streamlit/secrets.toml**: Gemini API 키를 안전하게 저장하는 파일입니다.

---

## 기타
- 질문/이슈는 [Streamlit Docs](https://docs.streamlit.io/) 및 [Google Generative AI Docs](https://ai.google.dev/)를 참고하세요. 