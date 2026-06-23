from llm import Qwen

model = Qwen()

while True:
    user_input = input("Input (type 'quit' to quit): ")
    if user_input.lower().strip() == "quit":
        print("Goodbye!")
        break
    else:
        print(f"Response: {model.chat(user_input)}")
