import os
from langchain_openai import ChatOpenAI
from load_dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, AIMessage, HumanMessage

load_dotenv()

chat = init_chat_model(
    'mimo-v2.5-pro',
    model_provider='openai',
    api_key=os.environ.get("MIMO_API_KEY"),
    base_url="https://token-plan-cn.xiaomimimo.com/v1"
)

_messages = [
    SystemMessage("你是一名来自边塞的诗人"),
    HumanMessage("帮我写一首诗"),
    AIMessage("锄禾日当午,汗滴禾下土,谁知盘中餐,粒粒皆辛苦"),
    HumanMessage("参照上面给的格式,再来一首")
]

resp = chat.stream(_messages)

for chunk in resp:
    print(chunk.content, end="", flush=True)

# chat = ChatOpenAI(
#     base_url="https://token-plan-cn.xiaomimimo.com/v1",
#     api_key=os.environ.get("MIMO_API_KEY"),
#     model="mimo-v2.5-pro"
# )

