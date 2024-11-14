from chairsapp.models import Order
import json
from bot.model import model, model_4o
from langchain_core.messages import HumanMessage
import base64

def order_status_agent(state):    
    response = model.invoke(f"""Analyse the sentence and check if there is any order number in the sentence and image location with the following rules:
                            
                            This is the response format: 'order_number:image_location:order_status'

                            If there is an order number in the sentence then in put the order number in the order_number place in the response format without any quotes.
                            the order number in the form of a string without any quotes.
                            
                            If there is an image location in the sentence then in put the image location in the image_location place in the response format without any quotes.

                            Analyse the meaning of the sentence and understand weather the user is asking for the status or refund and put the same in the order_status place in the response format without any quotes.
                            
                            If there is no order number in the sentence then return None.
                            
                            This is the sentence: ${state["question"]}""",)

    if response.content == "None":
        required_json = {
            "message": "Please provide a valid Order Number",
        }   

        return {"documents": json.dumps(required_json), "question": state["question"]}
    
    order_info = str(response.content)

    order_number = ""
    image_location = ""
    order_status = ""

    if ":" in order_info:
        order_number, image_location, order_status = order_info.split(":")

    try:
        order = Order.objects.get(order_number=order_number)

        if order_status == "status" or order_status == "order_status":
            required_json = {
                "message": f"The order status for the order number {order_number} is {order.order_status}",
            }

            return {"documents": json.dumps(required_json), "question": state["question"]}
        
        elif order_status == "refund" or order_status == "order_refund":
            if order.order_status == "refund":
                required_json = {
                    "message": "The order has already been refunded",
                    "type": "reply",
                }

                return {"documents": json.dumps(required_json), "question": state["question"]}

            if image_location == "" or image_location == "None" or image_location == "none":
                required_json = {
                    "message": "Please provide an image of the delivered shipment/package to check for damages",
                    "type": "image_input",
                    "order_number": order_number,
                }

                return {"documents": json.dumps(required_json), "question": state["question"]}
            
            else:
                required_json = {}

                with open(image_location, "rb") as image_file:
                    # Read the image
                    image = image_file.read()

                    # Encode the image into base64
                    image_base64 = base64.b64encode(image).decode("utf-8")

                    message = HumanMessage(
                    content=[
                            {"type": "text", "text": """
                                You are a very professional image analyzer, 
                                Check visually if product in the image provided to you is damaged or not

                                And return only one single word as the answer: 'refund' or 'replace' or 'needs_human_review'
                            """},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                            },
                        ],
                    )

                    response = model_4o.invoke([message])

                    if response.content == "refund":
                        order.order_status = "refund"
                        order.save()

                        required_json = {
                            "message": "Refund has been initiated for the order",
                            "type": "reply",
                        }

                    elif response.content == "replace":
                        order.order_status = "replace"
                        order.save()

                        required_json = {
                            "message": "Replace has been initiated for the order",
                            "type": "reply",
                        }

                    elif response.content == "needs_human_review":
                        order.order_status = "needs_human_review"
                        order.save()

                        required_json = {
                            "message": "The order needs human review",
                            "type": "reply",
                        }

                return {"documents": json.dumps(required_json), "question": state["question"]}
            
        else:
            required_json = {
                "message": f"The order status for the order number {order_number} is {order.order_status}",
            }

            return {"documents": json.dumps(required_json), "question": state["question"]}
    except Order.DoesNotExist:
        required_json = {
            "message": "The order number you provided is invalid. Please provide a valid Order Number",
        }

        return {"documents": json.dumps(required_json), "question": state["question"]}
    
    
    