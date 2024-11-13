from pydantic import BaseModel, Field
from typing import Literal
from bot.model import model

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["recommendation_agent", "order_status_agent", "fraud_detection_agent"] = Field(
        ...,
        description="Given a user question route it to recommendation_agent or order_status_agent or fraud_detection_agent",
    )

structured_llm_router = model.with_structured_output(RouteQuery)