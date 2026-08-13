from openai import OpenAI
import os
from load_dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    # base_url="https://ark.cn-beijing.volces.com/api/plan/v3",
    base_url="https://token-plan-cn.xiaomimimo.com/v1",
    # api_key=os.environ.get("ARK_API_KEY")
    api_key=os.environ.get("MIMO_API_KEY")
)

response = client.chat.completions.create(
    # model="doubao-seed-2.0-lite",
    model="mimo-v2.5-pro",
    messages=[
        { "role": "user", "content": "你是谁" }
    ],
    stream=False
)

print(response)