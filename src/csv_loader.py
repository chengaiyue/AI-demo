from langchain_community.document_loaders import CSVLoader


csv_loader = CSVLoader(
    file_path="./file_collection/demo.csv",
    csv_args={
        "delimiter": ',', # 分隔符
        "quotechar": '"', # 分隔符包裹
        "fieldnames": [] # 没有表头可以自己指定，有表头填写的话会把表头当成数据 
    },
    encoding="utf-8"
)

_document = csv_loader.load()

# for item in _document:
#     print(item)

for item in csv_loader.lazy_load():
    print(item)


# print(_document)

