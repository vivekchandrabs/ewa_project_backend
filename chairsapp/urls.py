# basic URL Configurations
from django.urls import include, path

# import everything from views
from chairsapp.views import AgentView
from chairsapp.order import OrderView
from chairsapp.farud import FraudDetectionController

# specify URL Path for rest_framework
urlpatterns = [
    path('ask/', AgentView.as_view(), name="agent_view"),
    path('api/order/', OrderView.as_view(), name="order_view"),
    path('api/fraud-order/', FraudDetectionController.as_view(), name="fraud_order_view"),
	path('api-auth/', include('rest_framework.urls'))
]
