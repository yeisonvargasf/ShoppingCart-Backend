from .views import CustomerViewSet, ProductViewSet, StockViewSet, OrderViewSet

# Third Parties Imports
from rest_framework.routers import DefaultRouter

my_routers = DefaultRouter()
my_routers.register(r'customers', CustomerViewSet)
my_routers.register(r'products', ProductViewSet)
my_routers.register(r'stocks', StockViewSet)
my_routers.register(r'orders', OrderViewSet)
