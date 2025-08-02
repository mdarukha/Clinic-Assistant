import os
import sys
import contextlib
from llama_cpp import Llama

# local path to mistral model
MODEL_PATH = os.path.join("models", "mistral-7b-instruct-v0.2.Q4_K_M.gguf")

# function to suppress model output for cleaner frontend deployment
@contextlib.contextmanager
def suppress_output():
    
    # suppres all model loading messages
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

# load model silently
with suppress_output():
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=4,
        temperature=0.6,
        top_k=50
    )

# prompt for assistant role
def format_prompt(query, context):
    return (
        "You are a helpful assistant at a medical clinic. "
        "You can answer questions about services, hours, insurance, and health topics.\n\n"
        f"Context: {context.strip()}\n\n"
        f"Question: {query.strip()}"
    )

def generate_response(query, context, max_tokens=200):
    prompt = format_prompt(query, context)

    with suppress_output():
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
        )

    return response["choices"][0]["message"]["content"].strip()