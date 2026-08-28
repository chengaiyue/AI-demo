import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from langchain_community.document_loaders import CSVLoader

from langchain_chroma import Chroma

openai_embeddings = OpenAIEmbeddings(
    model="doubao-embedding-vision",
    chunk_size=100,
    check_embedding_ctx_length=False, # 需要加这个参数，不然报错
    api_key=os.environ.get("EMBEDDING_MODEL_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/plan/v3",
)

vectorstore = Chroma(  # 内存向量存储
    collection_name='test',
    embedding_function=openai_embeddings,
    persist_directory='./chroma_db'
)

loader = CSVLoader(
    file_path="./file_collection/demo.csv",
    encoding="utf-8",
    source_column="name",
    metadata_columns=["name"],  # 只将 name 列添加到 metadata
)

documents = loader.load()

vectorstore.add_documents(
    documents=documents,
    ids=[str(f"id{i}") for i in range(len(documents))]
)

res = vectorstore.similarity_search(
    query="123456789",
    k=2,
    # filter={"name": "zcc"}
)

print(res)
