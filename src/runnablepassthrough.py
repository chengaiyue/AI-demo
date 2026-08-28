import os
from load_dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings

from langchain_core.vectorstores import InMemoryVectorStore

from langchain_core.runnables import RunnablePassthrough


chat = init_chat_model(
    "mimo-v2.5-pro",
    model_provider="openai",
    api_key=os.environ.get("MIMO_API_KEY"),
    base_url="https://token-plan-cn.xiaomimimo.com/v1",
)

openai_embeddings = OpenAIEmbeddings(
    model="doubao-embedding-vision",
    chunk_size=100,
    check_embedding_ctx_length=False, # 需要加这个参数，不然报错
    api_key=os.environ.get("EMBEDDING_MODEL_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/plan/v3",
)

vectorstore = InMemoryVectorStore(  # 内存向量存储
    embedding=openai_embeddings,
)

vectorstore.add_texts(["减肥就是要少吃多练", "减肥期间吃东西很重要", "跑步是很好的运动哦"])

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "只根据我提供的参考资料，简单明了的回答用户问题，参考资料：{context}"),
        ("human", "用户问题：{question}")
    ]
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

def fromat_fun(docs):
    reference_text = "["
    for doc in docs:
        reference_text += doc.page_content    
    reference_text += "]"
    return reference_text

def print_prompt(prompt):
    print(prompt)
    return prompt

chain = { "question": RunnablePassthrough(), "context": retriever | fromat_fun } | prompt | print_prompt | chat | StrOutputParser()

resp = chain.invoke("减肥期间应该注意什么")

print(resp)
