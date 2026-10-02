from sentence_transformers import SentenceTransformer
import chromadb, ollama, streamlit as st
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")
model = (load_model())
st.title("My chatbot ")
if "messages" not in st.session_state:
    st.session_state.messages = []
st.snow()
with st.sidebar:
    st.header(":blue[⚙️Chat Settings]")
    if st.button("📜💬Chat History"):
         for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    if st.button("Clear Chat 🗑️"):
            st.session_state.messages=[]
            st.success("Chat cleared")
    personalities = {
            "👶 Kid" : " answer the questions like explaining to a 5 year old kid. Give answer in 2 lines only",
            "😊 Friend" : "Answer the questions in a friendly and causal manner.give answer in 2 lines only",
            "👨‍🏫 Teacher": "Answer the questions ina friendly manner and professionally .give answer in 2 lines only",
            "🧑‍💻 Coder": "Answer programming questions clearly and simply.",
            "🧠 Expert": "Answer the questions with accurate and knowledgeable explanations."
        }
    personality = st.selectbox("select a personality", personalities.keys())
    uploaded_file = st.file_uploader("upload a file")
    if uploaded_file:
        text =uploaded_file.read().decode("UTF-8")
        with st.expander("Preview"):
            st.text(text)

        chunks = []
        chunk_size = 100
        chunk_overlap = 20
        step = chunk_size - chunk_overlap
        for i in range(0, len(text), step):
            chunk = text[i:i+chunk_size]
            chunks.append(chunk)
        embeddings = model.encode(chunks)
        client = chromadb.PersistentClient(path="./chromadb")
        collection = client.get_or_create_collection("my_documents")
        ids = []
        for i in range(len(chunks)):
            ids.append(f"{uploaded_file.name}_{i}")
        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings.tolist()
        )
#query phase
question =st.chat_input("Ask a question...")
if question:
    if uploaded_file:
        with st.chat_message("user"):
            st.write(question)
        question_embedding = model.encode(question)
        results = collection.query(
            query_embeddings=[question_embedding.tolist()],
            n_results=3
        )
        retrieved_results = results['documents'][0]
        retrieved_ids= results['ids'][0]

    #Prompting
        context = '\n'.join(retrieved_results)

        prompt = f'''
        Answer the question using the context provided below.context
        Question : {question}
        context : {context}
        Answer:
        '''
        print(prompt)
        #connecting to local model
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[{
                "role":"user",
                "content":prompt
            }]
        )
        with st.chat_message("assistant"):
            st.write(response["message"]["content"])
        with st.expander("Source"):
            for i in range(3):
                st.warning(
                    f"Chunk {i + 1}\n\n"
                    f"ID: {retrieved_ids[i]}\n\n"
                    f"{retrieved_results[i]}"
                )
    else:
        st.session_state.messages.append(
            {"role": "user",
            "content": question}
        )
        
        with st.chat_message("user"):
            st.write(question)
        with st.spinner("🧠🧠Thinking..."):
            response = ollama.chat(
            model="llama3.2:3b",
            messages=[{"role" : "system",
                 "content": personalities[personality]}] + st.session_state.messages)
        
            answer = response["message"]["content"]
        st.session_state.messages.append({

                "role": "assistant",
                "content": response["message"]["content"]
            })
        with st.chat_message("assistant"):
                st.write(response["message"]["content"])
        
        print("---- Chat history -----")
        for msg in st.session_state.messages:
             print(msg["role"], ":", msg["content"])