from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order  # Import the Order model
import random
from django.utils import timezone

class OrderView(APIView):
    def post(self, request):
        # Get the data from the request
        data = request.data
        
        # Extract individual fields from the request
        name = data.get('name')
        price = data.get('price')
        image = data.get('image')
        description = data.get('description')
        discount = data.get('discount', 0)  # Default discount is 0 if not provided
        has_rebate = data.get('has_rebate', False)
        chair_type = data.get('chair_type')
        
        # New fields for payment and shipping
        customer_name = data.get('customer_name')
        card_number = data.get('card_number')
        card_exp = data.get('card_exp')
        cvv = data.get('cvv')
        shipping_address = data.get('shipping_address')
        zip_code = data.get('zip_code')

        # Generate a random 6-digit order number
        order_number = str(random.randint(100000, 999999))

        # Validate required fields
        if not price:
            return Response({"error": "Price is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not chair_type:
            return Response({"error": "Chair type is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate card details (basic validation for length, further validation should be more complex in real-world applications)
        if card_number and len(card_number) != 12:
            return Response({"error": "Card number must be 16 digits"}, status=status.HTTP_400_BAD_REQUEST)
        if card_exp and len(card_exp) != 5:
            return Response({"error": "Card expiration must be in MM/YY format"}, status=status.HTTP_400_BAD_REQUEST)
        if cvv and len(str(cvv)) != 3:
            return Response({"error": "CVV must be 3 digits"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate final_price: price - (price * discount / 100)
        try:
            price = float(price)  # Convert to float if necessary
            discount = int(discount)  # Convert to integer if necessary
            final_price = price - (price * discount / 100)
        except ValueError:
            return Response({"error": "Invalid price or discount value"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Order instance
        try:
            order = Order.objects.create(
                name=name,
                price=price,
                final_price=final_price,  # Set the calculated final price
                image=image,
                description=description,
                discount=discount,
                has_rebate=has_rebate,
                chair_type=chair_type,
                order_number=order_number,
                order_creation_date=timezone.now(),
                customer_name=customer_name,
                card_number=card_number,
                card_exp=card_exp,
                cvv=cvv,
                shipping_address=shipping_address,
                zip_code=zip_code
            )
            
            # Prepare the order response data
            order_data = {
                'id': order.id,
                'name': order.name,
                'price': order.price,
                'final_price': order.final_price,  # Include the final price
                'image': order.image,
                'description': order.description,
                'discount': order.discount,
                'has_rebate': order.has_rebate,
                'chair_type': order.chair_type,
                'order_number': order.order_number,
                'order_creation_date': order.order_creation_date,
                'customer_name': order.customer_name,
                'shipping_address': order.shipping_address,
                'zip_code': order.zip_code,
                'order_status': order.order_status,
            }

            # Return the response in the specified format
            return Response({
                "order": order_data,
                "type": "confirmation"
            }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
