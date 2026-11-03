import ollama

print("Welcome to My AI Chatbot!")
print("Powered by Llama 3.2")
print("Type 'bye' to exit.\n")

while True:
    message = input("You: ")

    if message.lower() == "bye":
        print("Bot: Goodbye! Have a nice day!")
        break

    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {"role": "user", "content": message}
            ]
        )

        print("Bot:", response["message"]["content"])

    except Exception as e:
        print("Error:", e)
        