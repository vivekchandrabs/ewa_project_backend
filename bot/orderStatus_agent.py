from chairsapp.models import Order
import json
from bot.model import model

def order_status_agent(state):
    response = model.invoke(f"""Can you return only the order number from 
                            this sentence in the form of a string only without any quotes: The sentence {state['question']}
                            If there is no order number in the sentence then return None""",)

    if response.content == "None":
        required_json = {
            "message": "Please provide a valid Order Number",
        }   

        return {"documents": json.dumps(required_json), "question": state["question"]}

    try:
        order_number = str(response.content)
        
        order = Order.objects.get(order_number=order_number)
        response = model.invoke(f"""Construct a proper message under ten words for this order status: {order.order_status}""",)

        required_json = {
            "message": response.content,
        }

        return {"documents": json.dumps(required_json), "question": state["question"]}
    except Order.DoesNotExist:
        required_json = {
            "message": "The order number you provided is invalid. Please provide a valid Order Number",
        }

        return {"documents": json.dumps(required_json), "question": state["question"]}
    
    
    