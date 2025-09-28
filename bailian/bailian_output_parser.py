from langchain_core.output_parsers import JsonOutputParser, CommaSeparatedListOutputParser, StrOutputParser
from langchain.output_parsers import DatetimeOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from common.llm import llm

parser = DatetimeOutputParser()
format_instructions = parser.get_format_instructions()


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", f"你是一个专业的助手,按照以下格式返回结果{format_instructions}"),
        ("human", "{input}"),
    ]
)
chain = prompt | llm | parser

resp = chain.invoke(input="二零二五年九月二十八日晚上十点十八分")

print(resp)
