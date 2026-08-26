from langchain_community.document_loaders import JSONLoader


json_loader = JSONLoader(
    file_path="./file_collection/stu.json",
    jq_schema='.[1]',
    json_lines=False, # 文件里是不是每一行都是一个独立的json对象
    text_content=False # 抽取是是否是字符串
)

_document = json_loader.load()

print(_document)


