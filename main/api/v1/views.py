from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet

from main.models import Customer, Stock, Product, Order, OrderProduct
from .serializers import CustomerSerializer, StockSerializer, ProductSerializer, OrderSerializer

import decimal

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().filter(id__in=Stock.objects.filter(quantity__gte=1)
                                            .values_list('my_product', flat=True))


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @detail_route(methods=['post'])
    def add_product_cart(self, request, pk=None):
        current_order = self.get_object()
        current_stock = Stock.objects.filter(my_product_id=self.request.data.get('product_id', None)).first()

        if not current_stock or current_stock.quantity < 1:
            return Response(status=HTTP_400_BAD_REQUEST)

        current_order_product = OrderProduct.objects.filter(my_product_id=self.request.data.get('product_id', None),
                                                            my_order=current_order).first()

        if current_order_product:
            current_order_product.quantity += 1
        else:
            current_order_product = OrderProduct(my_product_id=self.request.data.get('product_id', None),
                                                 my_order=current_order, quantity=1)
        current_stock.quantity -= 1
        current_stock.save()
        current_order_product.save()

        return Response(status=HTTP_200_OK)

    @detail_route(methods=['post'])
    def remove_product_cart(self, request, pk=None):
        current_order = self.get_object()
        current_stock = Stock.objects.filter(my_product_id=self.request.data.get('product_id', None)).first()

        if not current_stock:
            return Response(status=HTTP_400_BAD_REQUEST)

        current_order_product = OrderProduct.objects.filter(my_product_id=self.request.data.get('product_id', None),
                                                            my_order=current_order).first()

        if not current_order_product:
            return Response(status=HTTP_400_BAD_REQUEST)

        if current_order_product.quantity is None or current_order_product.quantity < 1:
            return Response(status=HTTP_400_BAD_REQUEST)

        current_order_product.quantity -= 1
        current_order_product.save()
        current_stock.quantity += 1
        current_stock.save()

        return Response(status=HTTP_200_OK)

    @detail_route(methods=['get'])
    def get_resume_order(self, request, pk=None):
        total = decimal.Decimal(0.0)
        quantity = 0

        for item in OrderProduct.objects.filter(my_order=self.get_object()).exclude(quantity__lte=0):
            quantity += item.quantity
            total += item.quantity * item.my_product.price

        return Response({'quantity': str(total), 'total': str(quantity)}, status=HTTP_200_OK)
