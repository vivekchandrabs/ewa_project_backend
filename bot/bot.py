from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from typing import List
from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph, START

from bot.route import structured_llm_router
from bot.recommendation_agent import recommendation_agent
from bot.orderStatus_agent import order_status_agent
from bot.fraud_detection_agent import fraud_detection_agent

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
    """

    question: str
    generation: str
    documents: List[str]

def route_question(state):
    """
    Route question to RAG.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    system = """You are an expert at routing a user question to recommendation_agent or order_status_agent or fraud_detection_agent.
    
    The recommendation_agent can answer questions about chairs, types of chairs.
    Use the recommendation_agent for questions on chair topics.
    
    The order_status_agent can answer questions about order status 
    The order_status_agent can also be used by the user to provide an image of the delivered shipment/package to check for damages.
    Use the order_status_agent for questions on order status topics.
    """

    route_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{question}"),
        ]
    )

    question_router = route_prompt | structured_llm_router

    question = state["question"]
    source = question_router.invoke({"question": question})
    if source.datasource == "recommendation_agent":
        return "recommendation_agent"
    elif source.datasource == "order_status_agent":
        return "order_status_agent"
    elif source.datasource == "fraud_detection_agent":
        return "fraud_detection_agent"

def chair_agent():
    workflow = StateGraph(GraphState)
    # Define the nodes
    workflow.add_node("recommendation_agent", recommendation_agent)
    workflow.add_node("order_status_agent", order_status_agent)
    workflow.add_node("fraud_detection_agent", fraud_detection_agent)

    # Build graph
    workflow.add_conditional_edges(
        START,
        route_question,
        {
            "recommendation_agent": "recommendation_agent",
            "order_status_agent": "order_status_agent",
            "fraud_detection_agent": "fraud_detection_agent",
        },
    )

    workflow.add_edge( "recommendation_agent", END)
    workflow.add_edge( "order_status_agent", END)
    workflow.add_edge( "fraud_detection_agent", END)

    # Compile
    app = workflow.compile()

    return app


if __name__ == "__main__":
     while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        inputs = {
            "question": user_input
        }

        response = chair_agent().invoke(inputs)

        print(response["documents"])