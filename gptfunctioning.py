from gpt4all import GPT4All

model = GPT4All(model_name="llama-2-7b-chat.ggmlv3.q4_0.bin", n_threads=4, model_path="./gpt4all")

def chat_with_model(user_input):
    while True:

        if user_input.lower() == 'exit':
            break  # Exit the loop if the user types "exit"
        
        # Generate a response based on user input
        response = model.generate(prompt=user_input, temp=0, max_tokens=800)
        
        # Extract the model's reply
        model_reply = response.strip().split("Model:")[-1].strip()
        
        # Print the model's response
        print(f"Model: {model_reply}\n")

        return model_reply



#chat_with_model("write a text on drugs.")