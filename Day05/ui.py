import ollama
import streamlit as st
st.markdown("# 🤖✨ Welcome to My AI Chatbot! ✨🤖")
st.markdown("### 💬 Your AI Assistant 🚀")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("⚙️💫 Chat Settings")

    if st.button("🧹🗑️ Clear Chat"):
        st.session_state.messages = []
        st.success("✨ Chat cleared successfully! 🎉")

    st.divider()
    st.subheader("🎭 Choose AI Personality")

    personalities = {
        "👶 Kid": "Answer the questions like explaining to a 5 year old kid. Give the answer in 2 lines only.",
        "😊 Friend": "Answer the questions in a friendly and casual manner. Give the answer in 2 lines only.",
        "👨‍🏫 Teacher": "Answer the questions in a formal and educational manner. Give the answer in 2 lines only.",
        "🧑‍💻 Coder": "Answer programming questions clearly and simply.",
        "🧠 Expert": "Answer the questions with accurate and knowledgeable explanations."
    }

    personality = st.selectbox(
        "🎯 Select a personality",
        list(personalities.keys())
    )
    st.divider()
    st.subheader("📚 Upload File")

    uploaded_file = st.file_uploader(
        "📄 Upload a text file",
        type=["txt"]
    )
    context = ""
    if uploaded_file:
        st.success("✅ File uploaded successfully! 🎉")
        try:
            context = uploaded_file.read().decode("UTF-8")
            if st.button("👁️ Display File"):
                st.text_area(
                    "📖 File Content",
                    context,
                    height=250
                )
        except Exception:
            st.error("❌ File not supported!")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        avatar = "👤"
    else:
        avatar = "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
question = st.chat_input("💬✨ Ask me anything...")
if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })
    with st.chat_message("user", avatar="👤"):
        st.write(question)
    system_prompt = personalities[personality]
    if context:
        system_prompt += (
            "\n\n📚 Use this uploaded file as context:\n"
            + context
        )
    with st.spinner("🤔💭 AI is thinking..."):
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                }
            ] + st.session_state.messages
        )
    answer = response["message"]["content"]
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
    with st.chat_message("assistant", avatar="🤖"):
        st.write(answer)
st.divider()
st.subheader("📜💬 Chat History")
if st.session_state.messages:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.write("👤 **User:**", msg["content"])
        elif msg["role"] == "assistant":
            st.write("🤖 **AI:**", msg["content"])

else:
    st.info("💭 No chat history yet. Start chatting! 🚀")

print("📜 ===== CHAT HISTORY =====")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        print("👤 User:", msg["content"])
    else:
        print("🤖 AI:", msg["content"])

print("📜 =======================")