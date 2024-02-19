from django.shortcuts import redirect, get_object_or_404
import logging
from .models import Client, Product, Order
from datetime import datetime, timedelta
from django.core.files.storage import FileSystemStorage
from .forms import ProductForm
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
    product = Product.objects.filter(pk=id_product).first()
    context = {
        "product": product
    }
    return render(request, "hw2_app/product.html", context=context)


def client_products_sorted(request, id_client: int, days: int):
    product_set = []
    # now = datetime.now()
    # before = now - timedelta(days=days)
    period = datetime.now() - timedelta(days=days)
    client = Client.objects.filter(pk=id_client).first()
    orders = Order.objects.filter(client=client, order_date__gte=period).all()
    for order in orders:
        products = order.product.all()
        for product in products:
            if product not in product_set:
                product_set.append(product)
    return render(request, 'hw2_app/client_all_products_from_orders.html',
                  {'client': client, 'product_set': product_set, 'days': days})


# представление для ввода данных о продукте через форму и сохранение изображения продукта на сервер
def product_form(request, id_product: int):
    product = get_object_or_404(Product, pk=id_product)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product.title = request.POST["title"]
            product.description = request.POST["description"]
            product.price = request.POST["price"]
            product.count = request.POST["count"]
            image_product = form.cleaned_data['image_product']
            fs = FileSystemStorage()
            fs.save(image_product.name, image_product)  # сохранение image на сервер
            if "image_product" in request.FILES:
                product.image_product = request.FILES["image_product"]  # запись Image в переменную БД
            product.save()
            logger.info(f"Product {product.title} is changed successfully")
            return redirect("product", id_product=product.id)
    else:
        form = ProductForm()

    context = {
        "form": form,
        "product": product,
    }
    return render(request, "hw2_app/product_form.html", context=context)