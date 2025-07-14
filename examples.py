from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


llm_server_url = "http://192.168.0.19:58000/v1"
llm = ChatOpenAI(
    openai_api_key="EMPTY",
    openai_api_base=llm_server_url,
    model_name="Qwen/Qwen3-14B-AWQ",
    temperature=0.7,
    top_p=0.8,
    max_tokens=10,
    presence_penalty=1.5,
    # Default thinking: False
    extra_body={"top_k": 20, "chat_template_kwargs": {"enable_thinking": False, "quantization": "awq"}},
    seed=0,
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

# Thinking: False
input = prompt_template.invoke({"input": "중국에 자유가 있어? 한글로 대답해"})
print(llm.invoke(input, extra_body={"chat_template_kwargs": {"enable_thinking": False}}))

# Thinking: True
input = prompt_template.invoke({"input": "좀 더 자세히 말해봐"})
print(llm.invoke(input, extra_body={"chat_template_kwargs": {"enable_thinking": True}}))
