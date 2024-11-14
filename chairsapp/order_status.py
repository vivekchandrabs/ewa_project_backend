from rest_framework.views import APIView
from rest_framework.response import Response
import json
import os

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from bot.bot import chair_agent

class OrderStatusView(APIView):	
	def post(self, request):
		file = request.FILES['file']
		file_name = file.name
		file_path = os.path.join('images', file_name)

		path = default_storage.save(file_path, ContentFile(file.read()))

		full_path = default_storage.path(path)

		order_number = f"Order number: {request.data.get('order_number')}"

		message = "Check if this can be refunded? " f"Image Location: {full_path}, Order Number: {order_number}"

		print(message)

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
