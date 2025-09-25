from langchain_core.output_parsers import JsonOutputParser
from langchain.agents import initialize_agent, AgentType
from common.llm import create_calc_tools, llm, chat_prompt_template
from pydantic import BaseModel, Field


class Output(BaseModel):
    args: str = Field("工具的入参")
    result: str = Field("计算的结果")


parser = JsonOutputParser(pydantic_object=Output)
format_instructions = parser.get_format_instructions()

agent = initialize_agent(
    tools=create_calc_tools(),
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

output_parser = JsonOutputParser(
    agent=agent,
    output_parser=JsonOutputParser()
)


prompt = chat_prompt_template.format_prompt(
    role="计算",
    domain="使用工具进行计算",
    question=f"""
    请阅读下面的问题，并返回一个严格的JSON对象，不能使用Markdown代码块包裹！
    格式要求：
    {format_instructions}
    """
)


resp = agent.invoke(prompt)
print(resp)
print(resp["output"])

