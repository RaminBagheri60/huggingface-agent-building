from smolagents import LiteLLMModel

# Create a client, to talk to ollama
model = LiteLLMModel( 
    model_id="ollama_chat/qwen2:7b", # gemma3-lmstudio or any model you want
    api_base="http://127.0.0.1:11434", # client talks to this local API
    num_ctx=8192,  # sets the model's context window to 8,192 tokens
)

print("Model connected successfully")