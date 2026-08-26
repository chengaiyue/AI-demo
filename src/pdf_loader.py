from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", "。", "，", " ", ""]
)

pdf_loader = PyPDFLoader(
    file_path="",                             # PDF 文件路径
    extract_images=False,                     # 是否提取图片中的文字（需安装 pytesseract）
    text_splitter=text_splitter,              # 文本分割器，传入实例而非字符串
    password=None,                            # PDF 密码，加密 PDF 时传入
    pages_delimiter="\n\f",                   # 页面分隔符，默认换页符
    mode="page"
)

docs = pdf_loader.load()
