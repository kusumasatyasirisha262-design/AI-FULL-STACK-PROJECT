import ollama
msgs = [
    {"role": "system",
     "content": "Give the answers in simple terms."}
]
while True:
    question = input("You:")
    if question.lower() == "exit":
        break 
    msgs.append(
        {"role": "user",
         "content": question}
    )
    response = ollama.chat(
        model="llama3.2:3b",
        messages=msgs)
    msgs.append(
        {"role": "assistant",
         "content": response["message"]["content"]}
    )
    print("AI:", response["message"]["content"])
print("----Chat History----\n")
for msg in msgs:
    print(msg["role"],":",msg["content"])