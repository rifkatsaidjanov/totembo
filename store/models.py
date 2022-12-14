from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_list_by_category', kwargs={'pk': self.pk})


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default='Описания товара')
    quantity = models.PositiveIntegerField()
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = 'https://sarus.uz/public/files/img/news_1528793026.jpg'
        return url


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    shipping = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)

    @property
    def cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total = sum([product.total_price for product in order_products])
        return total

    @property
    def cart_products_quantity(self):
        order_products = self.orderproduct_set.all()
        total = sum([product.quantity for product in order_products])
        return total


class OrderProduct(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
