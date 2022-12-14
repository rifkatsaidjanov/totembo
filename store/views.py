from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .forms import *
from .models import Product, Category, Order, OrderProduct, Customer
from django.db.models import Q
from .utils import cart_data
from shop import settings
from datetime import datetime
from django.core.mail import send_mail
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from shop import settings
from .forms import *
from .models import Product, Category, Order, OrderProduct, Customer
from .utils import cart_data


class ProductList(ListView):
    model = Product
    extra_context = {
        'title': 'Главная страница',
        'send_form': SendCommentForm()
    }

    context_object_name = 'categories'
    template_name = 'store/product_list.html'

    def get_queryset(self):
        categories = Category.objects.all()
        data = []
        for category in categories:
            products = Product.objects.filter(
                category=category, is_published=True)[:4]

            data.append({
                'title': category.title,
                'products': products
            })

        return data

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context["title"] = 'Главная страница'

        return context


class ProductListByCategory(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/category_product_list.html'

    def get_queryset(self):
        sort_filed = self.request.GET.get('sorter')
        products = Product.objects.filter(category_id=self.kwargs['pk'])
        if sort_filed:
            products = products.order_by(sort_filed)

        return products


class SearchedProducts(ProductListByCategory):

    def get_queryset(self):
        searched_word = self.request.GET.get('q')
        products = Product.objects.filter(
            Q(name__contains=searched_word) |
            Q(description__contains=searched_word)
        )
        return products


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'


def cart(request):
    data = cart_data(request)
    context = {
        'cart_products_quantity': data['cart_products_quantity'],
        'order': data['order'],
        'items': data['products']
    }
    return render(request, 'store/cart.html', context=context)


def checkout(request):
    cart = cart_data(request)
    context = {
        'cart_products_quantity': cart['cart_products_quantity'],
        'order': cart['order'],
        'items': cart['products'],
        'customer_form': CustomerForm(),
        'shipping_form': ShippingForm()
    }

    return render(request, 'store/checkout.html', context=context)


def add_or_delete_product_from_cart(request, product_id, action):
    product = Product.objects.get(pk=product_id)
    key = str(product_id)

    if not request.user.is_authenticated:
        session = request.session
        cart = session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = session['cart'] = {}

        cart_product = cart.get(key)

        if action == 'add' and product.quantity > 0:
            if cart_product:
                cart_product['quantity'] += 1
            else:
                cart[key] = {
                    'quantity': 1
                }
            product.quantity -= 1

        elif action == 'delete':
            cart_product['quantity'] -= 1
            product.quantity += 1

            if cart_product['quantity'] <= 0:
                del cart[key]


        elif action == 'delate_all':
            quantity = cart_product['quantity']
            cart_product['quantity'] = 0
            product.quantity += quantity
            if cart_product['quantity'] <= 0:
                del cart[key]
        product.save()
        session.modified = True

    else:

        customer = request.user.customer

        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

        order_product, created = OrderProduct.objects.get_or_create(
            order=order, product=product)

        if action == 'add' and product.quantity > 0:
            order_product.quantity += 1
            product.quantity -= 1


        elif action == 'delate_all':
            quantity = order_product.quantity
            order_product.quantity = 0
            product.quantity += quantity


        elif action == 'delete':
            order_product.quantity -= 1
            product.quantity += 1

        product.save()
        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()

    next_page = request.META.get('HTTP_REFERER', 'product_detail')
    return redirect(next_page)


def process_order(request):
    transaction_id = datetime.now().timestamp()
    data = request.POST

    name = data['name']
    email = data['email']
    phone = data['phone']
    address = data['address']
    city = data['city']
    state = data['state']
    zipcode = data['zipcode']

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        shipping_info = ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode
        )

        order_data = cart_data(request)
        cart_total_price = order_data['order'].cart_total_price
        cart_products_quantity = order_data['order'].cart_products_quantity
        products = order_data['products']
        product_list = ''
        for item in products:
            product_list += f'{item.product.name}: {item.quantity} шт. {item.total_price}\n\n'

    else:
        customer, created = Customer.objects.get_or_create(
            name=name,
            email=email,
            phone=phone
        )

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        shipping_info = ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode
        )

        order_data = cart_data(request)
        cart_total_price = order_data['order']['cart_total_price']
        cart_products_quantity = order_data['order']['cart_products_quantity']
        products = order_data['products']
        product_list = ''

        for item in products:
            product_list += f'{item["product"]["name"]}: {item["quantity"]} шт. {item["total_price"]}\n\n'

    message_to_user = f"""Здраствуйте, {name}    
    
Ваш заказ (#{transaction_id}) принят на обработку.

Заказанные товары:

{product_list}

Общее количество товаров: {cart_products_quantity}
Обая стоимость товаров: {cart_total_price}

Для подтверждения заказа с вами свяжутся в ближайшее время. 
"""
    # send_mail(
    #     'Оформление заказа',
    #     message_to_user,
    #     settings.EMAIL_HOST_USER,
    #     [email]
    # )

    message_to_owner = f"""
Заказ #{transaction_id}

Заказанные товары: 


{product_list}

Общее количество товаров: {cart_products_quantity}
Общая стоимость товаров: ${cart_total_price}

Информация о покупателе: 

Имя: {name}
Email: {email}
Телефон: {data['phone']}
Адрес: {data['address']}
Город: {data['city']}
Регион: {data['state']}
Индекс: {data['zipcode']}
"""
    # send_mail(
    #     'Обработка заказа',
    #     message_to_owner,
    #     settings.EMAIL_HOST_USER,
    #     [settings.EMAIL_HOST_USER],
    # )

    if not request.user.is_authenticated:
        session = request.session
        cart = session.get(settings.CART_SESSION_ID)
        print(cart)
        del session['cart']
    else:
        customer = request.user.customer

        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

        order_product, created = OrderProduct.objects.get_or_create(
            order=order, )
        for product in order.orderproduct_set.all():
            product.delete()
        order.save()
    messages.success(request, 'Заказ успешно оформлен!!!')
    return redirect('product_list')


# --------------- Sent Comment Email --------
def send_comment(request):
    form = SendCommentForm(data=request.POST)
    if form.is_valid():
        data = request.POST
        email = data['email']
        comment = data['comment']
        send_mail(
            'Отзыв от пользователя',
            comment + f'\n\n\n{email}',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER]
        )
        messages.success(request, 'Отправлено успешно !!!')
        return redirect('product_list')


# --------------- USERS START ---------------


def user_form(request):
    login_form = LoginForm()
    registration_form = RegistrationForm()

    context = {
        'login_form': login_form,
        'registration_form': registration_form
    }

    return render(request, 'store/user_form.html', context)


def user_login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('product_list')
    else:
        messages.error(request, 'Неверное имя пользователя или пароль')
        return redirect('user_form')


def register(request):
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Отлично! Вы успршно зарегистрировались!')
    else:
        errors = form.errors
        messages.error(request, errors)
    return redirect('user_form')


def user_logout(request):
    logout(request)
    return redirect('product_list')


def profile(request):
    return render(request, 'store/profile.html')

# --------------- USERS END ---------------
