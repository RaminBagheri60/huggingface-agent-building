# Building Agents with Hugging Face

Personal learning repo for the [Hugging Face Agents Course](https://huggingface.co/learn/agents-course). The goal is to go from understanding agents and LLMs to running a local model in Python — the first building block before adding tools, memory, and workflows.

An AI agent is more than a chatbot. It combines:

- **LLM** — the brain
- **Tools** — the hands
- **Reasoning** — the logic
- **Actions** — the execution

This project starts with the LLM layer: connect Python to a local model using [Ollama](https://ollama.com) and Hugging Face's [`smolagents`](https://github.com/huggingface/smolagents).

---

## Quick Start

### Prerequisites

- [Ollama](https://ollama.com/download) installed
- Python 3.10+

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install smolagents[litellm]
```

### 2. Pull a local model

```bash
ollama pull qwen2:7b
```

### 3. Start the Ollama server

```bash
ollama serve
```

Ollama runs at `http://127.0.0.1:11434` by default.

### 4. Connect Python to the model

```bash
python main.py
```

Expected output:

```text
Model connected successfully
```

---

## How It Works

`main.py` creates a client that talks to Ollama — it does **not** load the model into Python. It sends prompts to the local Ollama API and receives responses.

```python
from smolagents import LiteLLMModel

model = LiteLLMModel(
    model_id="ollama_chat/qwen2:7b",
    api_base="http://127.0.0.1:11434",
    num_ctx=8192,
)
```

| Parameter | Purpose |
|-----------|---------|
| `model_id` | Model served by Ollama (`ollama_chat/` prefix for chat models) |
| `api_base` | Local Ollama server URL |
| `num_ctx` | Context window size in tokens (8192 here) |

**Stack:**

| Tool | Role |
|------|------|
| **Ollama** | Runs LLMs locally |
| **Qwen2 7B** | Local model (`qwen2:7b`) |
| **smolagents** | Hugging Face agent framework |
| **LiteLLM** | Connects Python to the Ollama API |

### Optional: chat in the terminal

```bash
ollama run qwen2:7b
```

---

## Project Structure

```text
huggingface-agent-building/
├── main.py              # Connect Python to Ollama via smolagents
├── requirements.txt     # Python dependencies
├── README.md
└── doc/                 # Course notes and summaries
    ├── 1-What is agents.md
    ├── 2-LLMs.md
    └── 3-Messages and special tokens.md
```

---

## Learning Notes

Course summaries live in [`doc/`](doc/). Each file links back to the official Hugging Face lesson.

| # | Topic | Notes |
|---|-------|-------|
| 1 | What are agents? | [doc/1-What is agents.md](doc/1-What%20is%20agents.md) |
| 2 | What are LLMs? | [doc/2-LLMs.md](doc/2-LLMs.md) · [Official lesson](https://huggingface.co/learn/agents-course/unit1/what-are-llms) |
| 3 | Messages & special tokens | [doc/3-Messages and special tokens.md](doc/3-Messages%20and%20special%20tokens.md) · [Official lesson](https://huggingface.co/learn/agents-course/unit1/messages-and-special-tokens) |

### Progress so far

**Unit 1 — Foundations**

- LLMs are decoder-based transformers that predict the next token autoregressively until an EOS token
- Chat UIs show messages, but the model receives one concatenated prompt each time — formatted by **chat templates**
- Messages use roles: `system`, `user`, `assistant`
- For agents, the **system message** defines behavior, available tools, and action formatting

**This repo (hands-on)**

- Local LLM running via Ollama
- Python connection established through `LiteLLMModel` in `main.py`

**Next in the course**

- Tools — extending the agent beyond text generation

---

## Why This Matters

Before adding tools, memory, search, or APIs, you need a working connection between your code and an LLM. This repo covers that first step.

Official course: [Hugging Face Agents Course](https://huggingface.co/learn/agents-course)
