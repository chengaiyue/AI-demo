from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate, MessagesPlaceholder

"""
ChatPromptTemplate: 支持注入任意数量的历史会话消息
    from_message: 可以接受一个list消息 
        MessagesPlaceholder("history"): 提供history作为占位的key, 基于invoke动态注入历史会话记录
"""


# 方式1：from_template 创建
# _template = PromptTemplate.from_template("我的名字叫:{name}")

# 方式2：构造函数创建
# _template = PromptTemplate(template="我的名字叫:{name}", input_variables=["name"])

# format 返回字符串
# print(_template.format(name="小明"))

# print(_template.invoke({ "name": "校长" }).text)

_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个边塞诗人，可以作诗"),
    ("human", "请在做一首诗"),
])

_template.messages.insert(1, MessagesPlaceholder(variable_name="history"))

history_data = [
    ("human", "你来写一首唐诗"),
    ("ai", "白发三千丈，高挂云间。"),
    ("human", "好诗，在来一首诗"),
    ("ai", "床前明月光，疑是地上霜。")
]

prompt_text = _template.invoke({ "history": history_data }).to_string()

print( prompt_text);


