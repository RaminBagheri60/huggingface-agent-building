# Building Agents with Hugging Face


An AI Agent is much more than just a chatbot.

It is the powerful combination of:

- 🧠 **LLM** — the brain
- 🛠️ **Tools** — the hands
- 🧐 **Reasoning** — the logic
- 🚀 **Actions** — the execution

This repository is about **building AI agents with Hugging Face**.

The first goal is simple:

> Run a local LLM on my own machine and connect it to Python using Hugging Face's `smolagents`.

---

## What We Are Building

In this first step, we will run a smart local model using:

- **Ollama** — to run LLMs locally
- **Qwen2 7B** — as the local model
- **smolagents** — Hugging Face's lightweight agent framework
- **LiteLLM** — to connect the local model to Python

`smolagents` is a simple library from Hugging Face for building AI agents with very little code.

You can think of it as a simpler alternative to frameworks like LangChain.

---

## Step 1: Install Ollama

Download and install Ollama:

https://ollama.com/download

Ollama allows you to run language models locally on your machine.

---

## Step 2: Pull a Local Model

Open your terminal and pull a lightweight model.

In this example, I am using `qwen2:7b`:

```bash
ollama pull qwen2:7b
```

---

## Step 3: Start the Ollama Server

Run Ollama in the background:

```bash
ollama serve
```

By default, Ollama runs on:

```text
http://127.0.0.1:11434
```

---

## Step 4: Install smolagents

Install Hugging Face's `smolagents` library with LiteLLM support:

```bash
pip install smolagents[litellm]
```

---

## Step 5: Connect Python to the Local Model

Create a Python file,to send prompt to Ollama:

```bash
main.py
```
Look at the code in this directory.
Notice we use LiteLLMModel class in the code. It creates a connection between
our Python program and the Ollama server running locally at http://127.0.0.1:11434. 

Run the file:

```bash
python main.py
```

If everything is working correctly, you should see:

```text
Model connected successfully!
```

---

### This object does not load the model into Python; it simply acts as a client that sends prompts to Ollama and receives the model's responses.

## Optional: Chat With the Model in Terminal

You can also run the model directly from the terminal:

```bash
ollama run qwen2:7b
```

Then you can start chatting with the model locally.

---

## Project Structure

A simple starting structure can look like this:

```text
building-agents-with-huggingface/
│
├── main.py
├── README.md
└── requirements.txt
```



## Why This Matters

This is the first building block of an AI agent.

Before adding tools, memory, search, APIs, or workflows, we first need to connect our Python code to an LLM.

After this step, we can start giving the agent real tools.


