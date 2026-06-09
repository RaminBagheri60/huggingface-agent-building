[What are LLMs?](https://huggingface.co/learn/agents-course/unit1/what-are-llms) from the Hugging Face Agents Course.


## Key Concepts

### What is an LLM?
- An AI model trained on large amounts of text to **understand and generate human language**
- Usually built on the **Transformer** architecture (since BERT, 2018)
- Works with **tokens** (sub-word units), not full words — e.g. `"interest"` + `"ing"` → `"interesting"`

### Three Transformer Types

| Type | Role | Examples | Typical use |
|------|------|----------|-------------|
| **Encoder** | Text → dense embedding | BERT | Classification, search, NER |
| **Decoder** | Generates tokens one at a time | Llama | Chat, code generation |
| **Encoder–Decoder** | Input → context → output | T5, BART | Translation, summarization |

Modern LLMs are usually **decoder-based** models with **billions of parameters** (GPT-4, Llama 3, Mistral, Gemma, SmolLM2, DeepSeek-R1, etc.).

### Core Mechanism: Next-Token Prediction
- The model predicts the **next token** given previous tokens
- It is **autoregressive**: each generated token becomes input for the next step
- Generation stops when the model outputs an **EOS (End of Sequence)** special token
- Decoding strategies range from simple (pick highest score) to advanced (e.g. beam search)

### Special Tokens
Each model family uses its own special tokens for structure (start/end of messages, turns, etc.), e.g.:
- GPT-4: `<|endoftext|>`
- Llama 3: `<|eot_id|>`
- SmolLM2: `<|im_end|>`

You don’t need to memorize them, but they matter for how prompts and outputs are formatted.

### Attention
- Transformers use **attention** to weigh which input tokens matter most when predicting the next token
- **Context length** = max tokens the model can process in one pass

### Prompting
- The input sequence is the **prompt**
- Because the model only predicts the next token, **how you phrase the prompt strongly shapes the output**

### Training
1. **Pre-training** — learn language patterns via next-token (or masked) prediction on huge text corpora  
2. **Fine-tuning** — specialize for chat, tools, code, classification, etc.

### How to Use LLMs
1. **Run locally** (if you have enough hardware)  
2. **Use a cloud/API** (e.g. Hugging Face Serverless Inference)

The course mainly uses **APIs on the Hugging Face Hub**; local usage comes later.

### LLMs in Agents
LLMs enable agents to:
- Interpret user instructions  
- Maintain conversational context  
- Plan and decide which tools to use  

**The LLM is the agent’s brain** — tools, reasoning, and actions build on top of it.

---
