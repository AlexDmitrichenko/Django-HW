import logging
from .models import Product, Client, Order
from datetime import datetime, timedelta
from django.shortcuts import render

logger = logging.getLogger(__name__)  # переменная для логирования


# вывод всех товаров
def products(request):
    products = Product.objects.all()
    logger.info(f'Страница "Список продуктов" успешно открыта')
    return render(request, 'hw2_app/products.html', {'products': products})


# вывод списка всех клиентов
def clients(request):
    clients = Client.objects.all()
    logger.info(f'Страница "Список клиентов" успешно открыта')
    return render(request, 'hw2_app/clients.html', {'clients': clients})


# вывод списка заказов
def orders(request):
    products_all = []
    orders = Order.objects.all()
    context = {
        'orders': orders
    }
    return render(request, 'hw2_app/orders_all.html', context=context)


def client_orders(request, id_client: int):
    products = {}
    client = Client.objects.filter(pk=id_client).first()
    orders = Order.objects.filter(client=client).all()

    for order in orders:
        products[order.id] = str(order.product.all()).replace('<QuerySet [<', '').replace('>]>',
                                                                                          '').split('>, <')

    return render(request, 'hw2_app/client_orders.html', {'client': client, 'orders': orders,
                                                          'products': products})


def product(request, id_product: int):
    products = Product.objects.filter(pk=id_product).first()
    context = {
        "product": products
    }
    return render(request, "hw2_app/products.html", context=context)


def client_products_sorted(request, id_client: int, days: int):
    product_set = []
    now = datetime.now()
    before = now - timedelta(days=days)
    client = Client.objects.filter(pk=id_client).first()
    orders = Order.objects.filter(client=client, order_date__range=(before, now)).all()
    for order in orders:
        products = order.product.all()
        for product in products:
            if product not in product_set:
                product_set.append(product)

    return render(request, 'hw2_app/client_all_products_from_orders.html',
                  {'client': client, 'product_set': product_set, 'days': days})
