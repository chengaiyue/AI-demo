from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import TextLoader

text_loader = TextLoader(
    file_path="",
    encoding="utf-8"
)

docs = text_loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,          # 每个分片的最大字符数
    chunk_overlap=200,        # 分片之间的重叠字符数，保证上下文连贯
    length_function=len,      # 计算长度的函数，默认 len
    separators=["\n\n", "\n", "。", "，", " ", ""]  # 分隔符优先级，从左到右尝试
)

split_docs = splitter.split_documents(docs)