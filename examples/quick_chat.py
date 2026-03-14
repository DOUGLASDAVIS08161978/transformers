#!/usr/bin/env python3
"""
Quickest way to chat with a transformer model - Just run and talk!
This is the simplest possible example to get started.
"""

from transformers import pipeline, Conversation

print("🤖 Loading chatbot... (first time may take a minute to download)")

# Create the chatbot - this is all you need!
chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

print("✨ Ready! Start chatting (type 'bye' to exit)\n")

# Create a conversation object to maintain context
conversation = Conversation()

while True:
    # Get your message
    user_input = input("You: ")

    # Exit if user says bye
    if user_input.lower() in ['bye', 'quit', 'exit']:
        print("👋 Goodbye!")
        break

    # Add your message and get response
    conversation.add_user_input(user_input)
    conversation = chatbot(conversation)

    # Print the bot's response
    print(f"🤖 Bot: {conversation.generated_responses[-1]}\n")
