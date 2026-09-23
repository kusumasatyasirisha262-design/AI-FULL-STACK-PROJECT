import ollama
question = input("Ask the question:")
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "system",
            "content": "Give answers in 2 lines only."
        },
        {
            "role": "user",
            "content": question
        }
    ]
)
print(response["message"]["content"])