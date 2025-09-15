from django.views import View
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from schedule.models import Product, Order
from .models import OrderItem


class HomePageView(View):
    def get(self, request):
        products = Product.objects.all()[:8]  # Показати лише перші 8 товарів
        return render(request, 'home.html', {
            'products': products,
            'show_catalog_btn': True,
        })


class ProductListView(View):
    def get(self, request):
        # Сортуємо продукти за назвою (можна поміняти на 'price')
        products = Product.objects.all().order_by('name')
        return render(request, 'products_list.html', {'products': products})


class ProductDetailView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        # шукаємо замовлення, де є цей продукт
        orders = Order.objects.filter(items__product=product).order_by('-created_at')

        return render(request, 'product_detail.html', {
            'product': product,
            'orders': orders,
        })


def get_or_create_order(request, customer):
    order_id = request.session.get("order_id")
    if order_id:
        try:
            return Order.objects.get(id=order_id, customer=customer, status="pending")
        except Order.DoesNotExist:
            pass
    order = Order.objects.create(customer=customer, status="pending")
    request.session["order_id"] = order.id
    return order


class AddToCartView(View):
    def post(self, request, product_id):

        customer, _ = Customer.objects.get_or_create(
            email="guest@example.com",
            defaults={"first_name": "Гість", "last_name": ""}
        )

        product = get_object_or_404(Product, id=product_id)
        order = get_or_create_order(request, customer)

        item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={"quantity": 1},
        )
        if not created:
            item.quantity += 1
            item.save()

        return redirect("cart_detail")


class CartDetailView(View):
    def get(self, request):
        customer, _ = Customer.objects.get_or_create(
            email="guest@example.com",
            defaults={"first_name": "Гість", "last_name": ""}
        )

        order = get_or_create_order(request, customer)
        items = order.items.select_related('product').all()
        total_price = sum(item.product.price * item.quantity for item in items)

        return render(request, 'cart_detail.html', {
            'order': order,
            'items': items,
            'total_price': total_price,
        })

