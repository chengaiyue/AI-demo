from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate

"""
ChatPromptTemplate: 支持注入任意数量的历史会话消息
    from_message: 可以接受一个list消息 
        MessagesPlaceholder("history"): 提供history作为占位的key, 基于invoke动态注入历史会话记录
"""


# 方式1：from_template 创建
_template = PromptTemplate.from_template("我的名字叫:{name}")

# 方式2：构造函数创建
# _template = PromptTemplate(template="我的名字叫:{name}", input_variables=["name"])

# format 返回字符串
print(_template.format(name="小明"))

print(_template.invoke({ "name": "校长" }).text)

ChatPromptTemplate.from_messages([

])


