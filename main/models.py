from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return '{0}'.format(self.name)


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(max_digits=20, decimal_places=0, blank=False, null=False)

    def __str__(self):
        return '{0}'.format(self.name)


class Stock(models.Model):
    my_product = models.OneToOneField(Product)
    quantity = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return 'Name: {0} - Quantity: {1}'.format(self.my_product.name, self.quantity)


class Order(models.Model):
    customer = models.ForeignKey(Customer, blank=False, null=False)
    products = models.ManyToManyField(Product, through='OrderProduct')

    def __str__(self):
        return '{0} {1}'.format(self.customer.name, self.id)


class OrderProduct(models.Model):
    my_product = models.ForeignKey(Product)
    my_order = models.ForeignKey(Order)
    quantity = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return 'Product: {0} - Customer: {1} - Quantity: {2}'.format(self.my_product.name, self.my_order.customer.name,
                                                                     self.quantity)
