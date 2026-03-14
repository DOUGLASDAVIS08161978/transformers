# Building Conversational AI with Transformers

This guide shows you how to create chatbots and conversational AI systems using the Hugging Face Transformers library - similar to how you interact with ChatGPT or Claude!

## Quick Start

### 1. Install Dependencies

```bash
pip install transformers torch
```

### 2. Run the Example

```bash
python examples/conversational_chatbot.py
```

## What You Can Build

### Simple Chatbots
- Customer service bots
- Personal assistants
- Educational tutors
- Entertainment/companion bots

### Advanced Applications
- Multi-turn conversations with memory
- Task-oriented dialogue systems
- Code assistants (like GitHub Copilot)
- Domain-specific AI assistants

## Available Models

### Lightweight (Good for Starting)
- **DialoGPT** (Microsoft): Conversational model, runs on CPU
- **BlenderBot** (Facebook): Engaging conversations
- **GPT-2**: Classic generative model

### Medium (Better Quality)
- **Llama-2-7b-chat**: Meta's chat model (requires approval)
- **Mistral-7B-Instruct**: High-quality instruction following
- **Falcon-7b-instruct**: Strong performance

### Large (Best Quality, Needs GPU)
- **Llama-2-13b/70b**: Larger variants
- **GPT-J/GPT-NeoX**: Open-source alternatives
- **Zephyr**: Fine-tuned for helpfulness

## Key Concepts

### 1. Tokenization
Converting text to numbers the model understands:
```python
tokenizer = AutoTokenizer.from_pretrained("model-name")
tokens = tokenizer.encode("Hello, how are you?")
```

### 2. Generation
Creating responses:
```python
output = model.generate(input_ids, max_length=100)
response = tokenizer.decode(output)
```

### 3. Context/Memory
Maintaining conversation history:
```python
# Keep track of previous messages
chat_history = []
chat_history.append({"role": "user", "content": user_input})
chat_history.append({"role": "assistant", "content": bot_response})
```

### 4. Parameters That Control Behavior

- **temperature**: Randomness (0.1 = focused, 1.0 = creative)
- **top_p**: Nucleus sampling (0.9-0.95 recommended)
- **max_length**: Maximum response length
- **do_sample**: Enable random sampling for variety

## Simple 5-Minute Example

```python
from transformers import pipeline

# Create chatbot
chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

# Have a conversation
from transformers import Conversation

conversation = Conversation("Hello! How are you?")
conversation = chatbot(conversation)

print(conversation.generated_responses[-1])
```

## Real-World Example: Customer Service Bot

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def customer_service_bot(user_message, history=None):
    """
    Simple customer service bot with conversation history
    """
    # Encode input
    new_input = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')

    # Combine with history
    if history is not None:
        bot_input = torch.cat([history, new_input], dim=-1)
    else:
        bot_input = new_input

    # Generate response
    history = model.generate(
        bot_input,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7,
        do_sample=True
    )

    # Decode response
    response = tokenizer.decode(history[:, bot_input.shape[-1]:][0], skip_special_tokens=True)

    return response, history

# Usage
history = None
response, history = customer_service_bot("I need help with my order", history)
print(response)

response, history = customer_service_bot("It hasn't arrived yet", history)
print(response)
```

## Using Different APIs

### 1. Pipeline API (Easiest)
```python
chatbot = pipeline("conversational")
```

### 2. Generate API (More Control)
```python
model.generate(input_ids, max_length=100, temperature=0.7)
```

### 3. Chat Template API (Modern Models)
```python
messages = [{"role": "user", "content": "Hello!"}]
prompt = tokenizer.apply_chat_template(messages)
```

## Tips for Better Conversations

1. **Use chat-tuned models**: Models with "chat" or "instruct" in the name
2. **Maintain context**: Keep conversation history for coherent responses
3. **Set appropriate parameters**: Lower temperature for factual, higher for creative
4. **Handle errors gracefully**: Add try-except blocks for production
5. **Limit context length**: Trim old messages to avoid memory issues

## Common Issues

### Out of Memory
- Use smaller models (DialoGPT-small instead of large)
- Reduce max_length
- Clear chat history periodically

### Slow Response
- Use GPU if available (`device=0`)
- Try smaller models
- Reduce generation length

### Repetitive Responses
- Increase temperature (try 0.8-0.9)
- Use top_p sampling
- Add repetition_penalty parameter

## Advanced: Creating a Web Interface

```python
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)
chatbot = pipeline("conversational")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    conversation = Conversation(user_message)
    conversation = chatbot(conversation)
    return jsonify({'response': conversation.generated_responses[-1]})

if __name__ == '__main__':
    app.run(port=5000)
```

## Resources

- [Hugging Face Model Hub](https://huggingface.co/models?pipeline_tag=conversational)
- [Transformers Documentation](https://huggingface.co/docs/transformers)
- [Generation Strategies Guide](https://huggingface.co/docs/transformers/generation_strategies)

## Next Steps

1. Run `conversational_chatbot.py` to try different examples
2. Experiment with different models
3. Adjust generation parameters
4. Build your own custom chatbot!
5. Deploy to a web app or API

Happy building! 🤖
