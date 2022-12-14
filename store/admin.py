from django.contrib import admin
from .models import Category, Product, Order, OrderProduct, Customer, ShippingAddress

admin.site.register(Category)
admin.site.register(ShippingAddress)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
