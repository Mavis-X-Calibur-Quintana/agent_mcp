from langchain_core.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain_experimental.tools.python.tool import PythonREPLTool

from common.llm import llm

tools = [PythonREPLTool()]
tool_names = ['PythonREPLTool']

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 创建提示词
prompt_template = PromptTemplate.from_template(template="""
尽你所能回答以下问题，你可以使用以下工具[{tool_names}]
--
请按照以下的格式进行思考：
```
# 思考的过程
- 问题：你必须回答的问题
- 思考：你考虑应该怎么做
- 行动：要采取的行动，应该是[{tool_names}]中的一个
- 行动输入：要传递给行动的参数
- 观察：行动的结果
... （这个思考/行动/行动输入/观察可以重复多次）
# 最终答案
对原始输入问题的最终答案
```
--
注意：
- PythonREPLTool工具的入参是python代码，不允许添加```py 等标记
-- 
要求：{input}
""")

prompt = prompt_template.format(
    tool_names=", ".join(tool_names),
    input="""
1.向 E:\python\project\.temp 目录下写入一个新文件，名称为index.html
2.写一个企业的官网
"""
)

print(prompt)

agent.invoke(prompt)
