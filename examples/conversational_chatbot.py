#!/usr/bin/env python3
"""
Simple conversational chatbot using Hugging Face Transformers
This demonstrates how to interact with language models similar to chatting with an AI assistant
"""

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

def simple_chatbot_example():
    """
    Basic example using a smaller model that can run on most hardware
    """
    print("Loading model... (this may take a moment)")

    # Using a smaller conversational model
    model_name = "microsoft/DialoGPT-medium"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    print("Chatbot ready! Type 'quit' to exit.\n")

    # Chat history for context
    chat_history_ids = None

    while True:
        # Get user input
        user_input = input("You: ")

        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break

        # Encode user input and add end-of-sequence token
        new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

        # Append to chat history
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

        # Generate response
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            top_p=0.92,
            top_k=50,
            temperature=0.7
        )

        # Decode and print response
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"Bot: {response}\n")


def conversational_pipeline_example():
    """
    Simpler approach using the conversational pipeline
    """
    print("Loading conversational pipeline...")

    # Use the conversational pipeline (easier API)
    chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

    print("Chatbot ready! Type 'quit' to exit.\n")

    from transformers import Conversation
    conversation = Conversation()

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break

        conversation.add_user_input(user_input)
        conversation = chatbot(conversation)

        print(f"Bot: {conversation.generated_responses[-1]}\n")


def advanced_chat_example():
    """
    More advanced example with better models (requires more resources)
    """
    print("Loading advanced model... (this requires significant RAM/GPU)")

    # You can use larger models like:
    # - "meta-llama/Llama-2-7b-chat-hf" (requires authentication)
    # - "mistralai/Mistral-7B-Instruct-v0.1"
    # - "tiiuae/falcon-7b-instruct"

    model_name = "microsoft/DialoGPT-large"  # Using larger DialoGPT for demo

    chatbot = pipeline(
        "conversational",
        model=model_name,
        device=0 if torch.cuda.is_available() else -1  # Use GPU if available
    )

    print(f"Using model: {model_name}")
    print(f"Device: {'GPU' if torch.cuda.is_available() else 'CPU'}")
    print("Chatbot ready! Type 'quit' to exit.\n")

    from transformers import Conversation
    conversation = Conversation()

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break

        conversation.add_user_input(user_input)
        conversation = chatbot(conversation)

        print(f"Bot: {conversation.generated_responses[-1]}\n")


def chat_with_instruct_model():
    """
    Example using instruction-tuned models (better for task-following)
    """
    print("Loading instruction-tuned model...")

    model_name = "HuggingFaceH4/zephyr-7b-beta"  # Good open-source chat model

    # Note: This requires significant resources
    pipe = pipeline(
        "text-generation",
        model=model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )

    messages = []

    print("Chat assistant ready! Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        prompt = pipe.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        outputs = pipe(
            prompt,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95
        )

        response = outputs[0]["generated_text"].split("<|assistant|>")[-1].strip()
        print(f"Bot: {response}\n")

        messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    print("=" * 60)
    print("Conversational AI with Hugging Face Transformers")
    print("=" * 60)
    print("\nChoose an example:")
    print("1. Simple chatbot (lightweight, runs on most hardware)")
    print("2. Pipeline-based chatbot (easier API)")
    print("3. Advanced chatbot (requires more resources)")
    print("4. Instruction-tuned model (best quality, needs GPU)")

    choice = input("\nEnter choice (1-4): ")

    if choice == "1":
        simple_chatbot_example()
    elif choice == "2":
        conversational_pipeline_example()
    elif choice == "3":
        advanced_chat_example()
    elif choice == "4":
        chat_with_instruct_model()
    else:
        print("Invalid choice. Running simple example...")
        simple_chatbot_example()
