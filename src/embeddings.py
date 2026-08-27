import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from langchain_community.document_loaders import CSVLoader

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

loader = CSVLoader(
    file_path="./file_collection/demo.csv",
    encoding="utf-8",
)

documents = loader.load()

vectorstore.add_documents(
    documents=documents,
    ids=[str(f"id{i}") for i in range(len(documents))]
)

res = vectorstore.similarity_search(
    query="123456789",
    k=1,
)

print(res)
