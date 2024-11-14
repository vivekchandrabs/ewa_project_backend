from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    temperature=0.3,
    model='gpt-4o-mini'
)

model_4o = ChatOpenAI(
    temperature=0.3,
    model='gpt-4o'
)