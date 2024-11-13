from rest_framework.views import APIView
from rest_framework.response import Response
import json

from bot.bot import chair_agent

class AgentView(APIView):	
	def post(self, request):
		message = request.data.get('message')

		response = chair_agent().invoke({"question": message})
	
		items = response.items()

		# Convert dict_items to a list
		items_list = list(items)

		# Access the second item
		second_item = items_list[1]

		# Extract the value (if needed)
		second_item_value = second_item[1]

		response_json = json.loads(second_item_value)
		
		return Response(response_json)
