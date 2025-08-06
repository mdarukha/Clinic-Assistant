import argparse
from llama_cpp import Llama

# initialize mistral model
llm = Llama(
    model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=20,
    verbose=True
)

# function to return response from baseline model
def generate_baseline_response(query):
    prompt = f"""You are a helpful assistant. Answer the following question as best as you can.

### Question:
{query}

### Answer:"""

    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.7,
        stop=["</s>"]
    )

    return response["choices"][0]["message"]["content"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="Query to ask the baseline model")
    args = parser.parse_args()
    query = args.query

    print(f"[Baseline Query]: {query}")
    response = generate_baseline_response(query)
    print(f"[Baseline Response]: {response}")

if __name__ == "__main__":
    main()