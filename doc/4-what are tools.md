[What are Tools?](https://huggingface.co/learn/agents-course/unit1/tools) from the Hugging Face Agents Course.

## Overview

Agents take **actions** through **Tools**. This lesson covers what tools are, how to design them well, and how to integrate them into an agent via the **system message**.

Give an agent the right tools — with clear descriptions — and you dramatically expand what it can do.

---

## Key Concepts

### What Is a Tool?
- A **tool is a function given to the LLM** that fulfills a **clear objective**
- You can create a tool for almost any use case
- A good tool **complements the LLM** — it does something the model alone cannot do reliably

### Common Tool Examples

| Tool | Description |
|------|-------------|
| **Web Search** | Fetch up-to-date information from the internet |
| **Image Generation** | Create images from text descriptions |
| **Retrieval** | Retrieve information from an external source (RAG) |
| **API Interface** | Interact with external APIs (GitHub, YouTube, Spotify, etc.) |

### Why LLMs Need Tools
- LLMs only know what was in their **training data** — they cannot know today's weather or live stock prices on their own
- Without a search tool, asking for today's weather may cause **hallucinations**
- A **calculator tool** gives better arithmetic than relying on the model's internal math

### What Every Tool Should Include

| Component | Purpose |
|-----------|---------|
| **Description** | Text explaining what the function does |
| **Callable** | The actual code that performs the action |
| **Arguments** | Input parameters with types |
| **Outputs** *(optional)* | Return type(s) with types |

---

## How Tools Work

LLMs only accept **text in** and produce **text out**. They cannot call functions directly.

**The agent loop:**

1. You describe tools to the LLM in the system prompt
2. User asks a question (e.g. "What's the weather in Paris?")
3. LLM recognizes a tool is needed and **generates a text-based tool call**, e.g. `call weather_tool('Paris')`
4. The **Agent** (not the LLM) parses that response, runs the tool, and gets real data
5. Agent appends the tool result as a new message and passes the updated conversation back to the LLM
6. LLM generates a natural answer for the user

From the user's perspective, the LLM "used" the tool. In reality, the **agent orchestrated everything** in the background. Tool-calling steps are usually hidden from the user.

```
User: "What's the weather in Paris?"
        ↓
LLM:  call weather_tool('Paris')          ← text output, not a real function call
        ↓
Agent: executes weather_tool('Paris') → {"temp": 18, "condition": "cloudy"}
        ↓
LLM:  "It's 18°C and cloudy in Paris."
        ↓
User sees only the final answer
```

---

## Giving Tools to an LLM

Tools are described in the **system prompt**. Descriptions must be precise about:

1. **What the tool does**
2. **What exact inputs it expects**

Formats like JSON or structured text work well — any **precise, consistent format** is fine.

### Manual Tool Description (Calculator Example)

```python
def calculator(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b
```

| Field | Value |
|-------|-------|
| Name | `calculator` |
| Description | Multiply two integers |
| Arguments | `a: int`, `b: int` |
| Output | `int` (product of `a` and `b`) |

Text string for the LLM:

```text
Tool Name: calculator, Description: Multiply two integers., Arguments: a: int, b: int, Outputs: int
```

When this string is in the system prompt, the model knows the tool exists, what inputs to pass, and what output to expect.

**Problem:** Manual descriptions are fragile — easy to miss details or be inconsistent across multiple tools.

---

## Auto-Formatting Tool Descriptions

Python functions already encode everything needed:

- **Name** → function name (`calculator`)
- **Description** → docstring (`"""Multiply two integers."""`)
- **Arguments** → type hints (`a: int, b: int`)
- **Output** → return annotation (`-> int`)

The implementation details don't matter to the LLM — only name, description, inputs, and output.

### The `@tool` Decorator

With introspection (`inspect` module), a decorator builds the description automatically:

```python
@tool
def calculator(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

print(calculator.to_string())
# Tool Name: calculator, Description: Multiply two integers., Arguments: a: int, b: int, Outputs: int
```

Requirements for auto-formatting:
- **Type hints** on parameters and return value
- **Docstring** describing what the tool does
- **Sensible function name**

---

## Generic `Tool` Class

> Example from the course — fictional but similar to real library implementations.

```python
from typing import Callable

class Tool:
    def __init__(self, name: str, description: str, func: Callable,
                 arguments: list, outputs: str):
        self.name = name
        self.description = description
        self.func = func
        self.arguments = arguments
        self.outputs = outputs

    def to_string(self) -> str:
        args_str = ", ".join([
            f"{arg_name}: {arg_type}" for arg_name, arg_type in self.arguments
        ])
        return (
            f"Tool Name: {self.name},"
            f" Description: {self.description},"
            f" Arguments: {args_str},"
            f" Outputs: {self.outputs}"
        )

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
```

| Attribute / Method | Role |
|------------------|------|
| `name` | Tool identifier |
| `description` | What the tool does |
| `func` | Callable to execute |
| `arguments` | List of `(param_name, param_type)` pairs |
| `outputs` | Return type |
| `__call__()` | Runs the underlying function |
| `to_string()` | Produces the LLM-facing description string |

Manual instantiation:

```python
calculator_tool = Tool(
    "calculator",
    "Multiply two integers.",
    calculator,
    [("a", "int"), ("b", "int")],
    "int",
)
```

### The `@tool` Decorator (Implementation)

Uses `inspect.signature()` to extract types and `func.__doc__` for the description:

```python
import inspect

def tool(func):
    signature = inspect.signature(func)
    arguments = []
    for param in signature.parameters.values():
        annotation_name = (
            param.annotation.__name__
            if hasattr(param.annotation, '__name__')
            else str(param.annotation)
        )
        arguments.append((param.name, annotation_name))

    return_annotation = signature.return_annotation
    outputs = (
        return_annotation.__name__
        if hasattr(return_annotation, '__name__')
        else str(return_annotation)
        if return_annotation is not inspect._empty
        else "No return annotation"
    )

    return Tool(
        name=func.__name__,
        description=func.__doc__ or "No description provided.",
        func=func,
        arguments=arguments,
        outputs=outputs,
    )
```

The resulting `to_string()` output is **injected into the system prompt** as `tools_description`, alongside behavior instructions.

---

## Model Context Protocol (MCP)

[MCP](https://huggingface.co/learn/mcp-course/) is an **open protocol** that standardizes how apps provide tools to LLMs.

| Benefit | Description |
|---------|-------------|
| Pre-built integrations | Plug-and-play tools for LLMs |
| Vendor flexibility | Swap LLM providers without rewriting tool interfaces |
| Security | Best practices for keeping data in your infrastructure |

Any framework that implements MCP can reuse tools defined in the protocol — no need to reimplement the same interface per framework.

---

## Takeaways

- **Tools = functions** that extend what an LLM can do (calculate, search, call APIs, retrieve data)
- **LLMs don't call tools** — they output text; the **agent** parses, executes, and feeds results back
- **System prompt** carries tool descriptions; precision on inputs and behavior is critical
- **Auto-formatting** via `@tool` + type hints + docstrings avoids fragile manual strings
- **MCP** provides a unified, reusable tool interface across frameworks

**Next in the course:** [Agent Workflow](https://huggingface.co/learn/agents-course/unit1/agent-steps-and-structure) — how an agent observes, thinks, and acts (bringing LLMs, messages, and tools together).

---
