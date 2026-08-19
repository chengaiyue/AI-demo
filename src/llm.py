
import os
from langchain_openai import ChatOpenAI
from load_dotenv import load_dotenv;

load_dotenv()

llm = ChatOpenAI(
    base_url="https://token-plan-cn.xiaomimimo.com/v1",
    api_key=os.environ.get("MIMO_API_KEY"),
    model="mimo-v2.5-pro"
)

# ai_msg = llm.invoke([
#     ("user", "你是谁")
# ])

ai_msg = llm.stream([
    ("user", "你是谁")
])

full_response = ""
for chunk in ai_msg:
    print(chunk.content, end="", flush=True)
    full_response += chunk.content
print()  # 换行
print("完整回复:", full_response)
