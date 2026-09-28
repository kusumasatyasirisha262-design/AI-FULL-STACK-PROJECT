import ollama
import streamlit as st
st.markdown("# Welcome to my Chatbot App!!!")
with st.sidebar:
    st.header(":blue[Chat Settings]")
    if st.button("clear Chat🗑️"):
        st.session_state.messages=[]
        st.success("Chat cleared")
    personalities = {
        "kid" : " answer the questions like explaining to a 5 year old kid. Give answer in 2 lines only",
        "Friend" : "Answer the questions in a friendly and causal manner.give answer in 2 lines only",
        "Teacher" : "Answer the questions in a formal and educational manner. Give answer in 2 lines only",
    }
    personality = st.selectbox("select a personality", personalities.keys())
    uploaded_file = st.file_uploader("uploaded a text file...")
    try:
        if uploaded_file:
            st.write("File uploaded successfully")
            context = uploaded_file.read().decode("UTF-8")
            if st.button("Display"):
                st.text(context)   
    except:
        st.error("File not supported")
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
question = st.chat_input("You:")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })
    with st.chat_message("user"):
        st.write(question)
    with st.spinner("Thinking..."):
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {"role" : "system","content": personalities[personality]}]
                + st.session_state.messages)

    answer = response["message"]["content"]
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
    with st.chat_message("assistant"):
        st.write(answer)

    print("---- Chat history -----")
    for msg in st.session_state.messages:
        print(msg["role"], ":", msg["content"])