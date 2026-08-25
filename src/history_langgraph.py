"""
历史对话 - LangGraph Persistence 实现
"""

import os
from load_dotenv import load_dotenv

from langchain.chat_models import init_chat_model

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()

chat = init_chat_model(
    'mimo-v2.5-pro',
    model_provider='openai',
    api_key=os.environ.get("MIMO_API_KEY"),
    base_url="https://token-plan-cn.xiaomimimo.com/v1"
)


# 1. 定义节点：调用模型
def call_model(state: MessagesState):
    response = chat.invoke(state["messages"])
    return {"messages": [response]}


# 2. 构建图
builder = StateGraph(MessagesState)
builder.add_node("chat", call_model)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)

# 3. 编译时挂载 checkpointer（替代 InMemoryChatMessageHistory）
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 4. 调用（thread_id 等同于 session_id）
config = {"configurable": {"thread_id": "user_001"}}

graph.invoke({"messages": [HumanMessage(content="小明有一只猫")]}, config)
graph.invoke({"messages": [HumanMessage(content="小明有一条狗")]}, config)
res = graph.invoke({"messages": [HumanMessage(content="小明有几个宠物？")]}, config)

print(res["messages"][-1].content)
