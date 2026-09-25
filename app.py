import streamlit as st
from dotenv import load_dotenv

from src.task10_generation import generate_with_citation


load_dotenv()

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("RAG Chatbot")
    st.caption("Academic policy and news assistant")
    top_k = st.slider("Số chunks", 3, 10, 5)

st.title("RAG Chatbot")
st.caption("Hỏi về chính sách, học bổng, ký túc xá và cập nhật tin tức")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            for source in message["sources"][:3]:
                st.caption(f"Source: {source['metadata']['title']} ({source['retrieval_method']}, score={source['score']:.3f})")

query = st.chat_input("Nhập câu hỏi...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        result = generate_with_citation(query, top_k=top_k)
        answer = result["answer"]
        sources = result.get("sources", [])
        st.markdown(answer)
        if sources:
            for item in sources[:3]:
                metadata = item.get("metadata", {})
                st.caption(f"[{metadata.get('title', 'Unknown')} | {item.get('retrieval_method', 'unknown')}] score={item.get('score', 0):.3f}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })
