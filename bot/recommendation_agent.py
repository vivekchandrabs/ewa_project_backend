from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage

from bot.vectorStore import get_vector_store, get_retriever
from bot.model import model

chat_history = []

def recommendation_agent(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a friendly salesmen who is trying to help a customer with their questions. You are supposed to sell chairs with in the given data. 
        If you dont have the product which the customer is looking for, you can tell them that you dont have the product.
        Return all the information from the file about the chairs. Return the all the information in the json format and do not add any markdown formatting for the output.
        Return only the product information which the customer is looking for and do not return any other statements.

        If you receive any questions among the following, you can return the statements.

        1. Hello, I am looking for a chair.
        2. Hello.
        3. How are you?
         
        For any statements type questions send the response in the following format: 
        The json should contain a key called "message" and the value should be the response to the question.
        THe json should contain a key called "type" and the value should be 'reply'.

        For any product related information send the response in the following format:
        The json should contain a key called "products" and the value should be the list of products.
        The json should contain a key called "type" and the value should be 'product'.
         
        For the type of chairs response send the response in the following format:
        The json should contain a key called "chair_types" and the value should be the list of types of chairs.
        The json should contain a key called "type" and the value should be 'types'.
        
        Before showing any chairs ask the user if they are looking for a specific type of chair. 
        If they are looking for a specific type of chair, ask them the type of chair they are looking for.

        If they ask: What are the types of chairs you have?
        Return back all the type of chairs that are there in the document.

        If they ask: Show all the chairs that you have.
        Return back only the type of chairs that are there in the document.
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    retriever_tools = create_retriever_tool(
        get_retriever(get_vector_store("bot/data.json")),
        "chair_search",
        "Use this tool when searching for all the information about the chairs."
    )
    
    tools = [retriever_tools]
    agent = create_openai_functions_agent(
        llm=model,
        prompt=prompt,
        tools=tools
    )

    agentExecutor = AgentExecutor(agent=agent, tools=tools)

    response = agentExecutor.invoke({
        "input": state["question"],
        "chat_history": chat_history
    })

    chat_history.append(HumanMessage(content=state["question"]))
    chat_history.append(AIMessage(content=response["output"]))

    return {"documents": response["output"], "question": state["question"]}