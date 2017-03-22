from rest_framework.serializers import ModelSerializer, SerializerMethodField

from main.models import Customer, Product, Stock, Order, OrderProduct


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        ordering = ('id',)
        fields = ('id', 'name')


class ProductSerializer(ModelSerializer):

    stock = SerializerMethodField()

    class Meta:
        model = Product
        ordering = ('id',)
        fields = ('id', 'name', 'price', 'stock')

    def get_stock(self, current_product):
        return StockSerializer(Stock.objects.filter(my_product=current_product).first()).data


class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        ordering = ('id',)
        fields = ('my_product_id', 'quantity',)


class OrderProductSerializer(ModelSerializer):
    my_product = ProductSerializer()

    class Meta:
        model = OrderProduct
        ordering = ('my_order_id',)
        fields = ('my_order_id', 'my_product', 'quantity')


class OrderSerializer(ModelSerializer):
    customer = CustomerSerializer()
    products = SerializerMethodField()

    class Meta:
        model = Order
        ordering = ('id',)
        fields = ('id', 'customer', 'products')

    def get_products(self, order):
        my_products = OrderProduct.objects.filter(my_order=order).exclude(quantity__lte=0)
        return OrderProductSerializer(my_products, many=True).data
