FROM vllm/vllm-openai:v0.8.5

# Some new models may only be available on the main branch of HF Transformers.
RUN uv pip install --system git+https://github.com/huggingface/transformers.git