from langchain_core.messages import HumanMessage
from bot.model import model

import base64

# This function is used to detect fraud in the shipment
# It takes in the location of the image and converts the same into a base64 string
# The base64 string is then passed to the model to detect fraud
# The model returns a response which is then returned to the user.
def fraud_detection_agent(state):
    # Get the location of the image
    image_location = state["image_location"]

    message = None

    return {"documents": {"message": image_location}, "question": state["question"]}

    # # Open the image in binary mode
    # with open(image_location, "rb") as image_file:
    #     # Read the image
    #     image = image_file.read()

    #     # Encode the image into base64
        
    #     image_base64 = base64.b64encode(image).decode("utf-8")

    #     message = HumanMessage(
    #     content=[
    #             {"type": "text", "text": "Describe the image provided to you and tell me if you think it is damaged or not."},
    #             {
    #                 "type": "image_url",
    #                 "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
    #             },
    #         ],
    #     )

    #     response = model.invoke([message])

    #     return {"documents": response.content, "question": state["question"]}
