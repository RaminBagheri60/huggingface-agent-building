[Messages and Special Tokens](https://huggingface.co/learn/agents-course/unit1/messages-and-special-tokens) from the Hugging Face Agents Course.

## Key Concepts

### Chat UI vs. What the Model Sees
- Chat interfaces (ChatGPT, HuggingChat) show **messages**, but the LLM does not "remember" conversations
- Before inference, all messages are **concatenated into a single prompt string** and fed to the model in full every time
- **Chat templates** bridge the gap between conversational messages and the formatted prompt each model expects

### Special Tokens in Conversations
- Just as each LLM has its own **EOS token**, each model uses different **formatting rules and delimiters** for user/assistant turns
- Chat templates ensure every model receives a correctly formatted prompt despite these differences

## Message Types

### System Messages
- Also called **system prompts** — persistent instructions that define how the model should behave
- Shape tone, role, and behavior across the entire conversation
- In **Agents**, system messages also describe available tools, action formatting rules, and how to structure the thought process

```python
system_message = {
    "role": "system",
    "content": "You are a professional customer service agent. Always be polite, clear, and helpful."
}
```

### User and Assistant Messages
- A conversation is an alternating list of **user** and **assistant** turns
- Chat templates preserve conversation history so multi-turn exchanges stay coherent
- The template converts a Python list of message dicts into a single prompt string

```python
conversation = [
    {"role": "user", "content": "I need help with my order"},
    {"role": "assistant", "content": "I'd be happy to help. Could you provide your order number?"},
    {"role": "user", "content": "It's ORDER-123"},
]
```

### Same Conversation, Different Formats
The same message list is formatted differently depending on the model:

**SmolLM2** uses a simple role/content layout:
```
system
You are a helpful AI assistant named SmolLM, trained by Hugging Face
user
I need help with my order
assistant
I'd be happy to help. Could you provide your order number?
user
It's ORDER-123
assistant
```

**Llama 3.2** wraps each turn with its own special tokens and structure — the content is the same, but the delimiters differ.

## Chat Templates

### Base Models vs. Instruct Models

| Type | Description | Example |
|------|-------------|---------|
| **Base Model** | Trained on raw text to predict the next token | `SmolLM2-135M` |
| **Instruct Model** | Fine-tuned to follow instructions and hold conversations | `SmolLM2-135M-Instruct` |

- To make a base model behave like a chat model, prompts must be formatted consistently — that's what chat templates do
- **ChatML** is a common format using clear role indicators (`system`, `user`, `assistant`)
- When using an instruct model, always use the **correct chat template** for that model

### How Chat Templates Work
- In `transformers`, chat templates are **Jinja2 templates** that convert a list of JSON messages into the textual prompt a model expects
- Each instruct model may use a different conversation format and special tokens
- `transformers` applies the template automatically during tokenization — you only need to structure messages correctly
- In transformers, chat templates include Jinja2 code 

Simplified SmolLM2 template logic:
```jinja2
{% for message in messages %}
{{ message['role'] }}
{{ message['content'] }}
{% endfor %}
```

### Converting Messages to a Prompt
Use the model's tokenizer and `apply_chat_template()`:

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-1.7B-Instruct")
rendered_prompt = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
```

- `tokenize=False` — returns a string instead of token IDs
- `add_generation_prompt=True` — appends the assistant turn marker so the model knows where to start generating
- The returned `rendered_prompt` is ready to pass directly to the model
- APIs use this function behind the scenes when you send messages in ChatML format

## Takeaways for Agents
- Always structure input as a list of `{"role": ..., "content": ...}` messages
- Let the tokenizer's chat template handle model-specific formatting — don't hand-craft prompts for each model
- System messages are especially important for agents: they define behavior, tools, and action formats
- Next up in the course: how agents use **Tools** to act beyond text generation

---
