import os
from load_dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, AIMessage, HumanMessage

from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

load_dotenv()

_template = PromptTemplate.from_template("单词:{word}, 反义词:{antonyn}")

_example_data = [
    { "word": "正", "antonyn": "反" },
    { "word": "大", "antonyn": "小" }
]

few_shot_template = FewShotPromptTemplate(
    examples=_example_data,
    example_prompt=_template,
    prefix="请根据示例给出反义词：",
    suffix="单词:{word}, 反义词是？",
    input_variables=["word"]
)

chat = init_chat_model(
    'mimo-v2.5-pro',
    model_provider='openai',
    api_key=os.environ.get("MIMO_API_KEY"),
    base_url="https://token-plan-cn.xiaomimimo.com/v1"
)

prompt_text = few_shot_template.invoke({ "word": "好" }).to_string()

print("=== 拼接的 Prompt ===")
print(prompt_text)
print("\n=== LLM 回答 ===")

resp = chat.stream([HumanMessage(prompt_text)])

for chunk in resp:
    print(chunk.content, end="", flush=True)
print()