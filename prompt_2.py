import ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "system",
            "content": "Give answers in 2 lines only."
        },
        {
            "role": "user",
            "content": "Explain machine learning in 40 words"
        }
    ]
)
print(response["message"]["content"])