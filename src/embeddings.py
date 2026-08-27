import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from langchain_core.document_loaders import CSVLoader

from langchain_chroma import Chroma

openai_embeddings = OpenAIEmbeddings(
    model="doubao-embedding-vision",
    chunk_size=100,
    chunk_overlap=0,
    api_key=os.environ.get("EMBEDDING_MODEL_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/plan/v3",
)

vectorstore = InMemoryVectorStore(  # 内存向量存储
    embeddings=openai_embeddings,
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

