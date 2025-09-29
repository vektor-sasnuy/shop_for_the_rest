from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from schedule.models import Product, Order, Customer
from .models import OrderItem


# ---------- helpers ----------
def _get_guest(request):
    customer, _ = Customer.objects.get_or_create(
        email="guest@example.com",
        defaults={"first_name": "Гість", "last_name": ""}
    )
    return customer

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

# ---------- pages ----------
class HomePageView(View):
    def get(self, request):
        products = Product.objects.all()[:8]
        return render(request, "home.html", {"products": products, "show_catalog_btn": True})

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all().order_by("name")
        return render(request, "products_list.html", {"products": products})

class ProductDetailView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        orders = Order.objects.filter(items__product=product).order_by("-created_at")
        return render(request, "product_detail.html", {"product": product, "orders": orders})

# ---------- cart ----------
class AddToCartView(View):
    def post(self, request, product_id):
        customer = _get_guest(request)
        product = get_object_or_404(Product, id=product_id)
        if product.stock <= 0:
            return redirect("cart_detail")
        order = get_or_create_order(request, customer)
        item, created = OrderItem.objects.get_or_create(
            order=order, product=product, defaults={"quantity": 1}
        )
        if not created and item.quantity < product.stock:
            item.quantity += 1
            item.save()
        return redirect("cart_detail")

class UpdateCartItemView(View):
    def post(self, request, item_id):
        customer = _get_guest(request)
        order = get_or_create_order(request, customer)
        item = get_object_or_404(OrderItem, id=item_id, order=order)
        action = request.POST.get("action")
        if action == "inc" and item.quantity < item.product.stock:
            item.quantity += 1
            item.save()
        elif action == "dec":
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()
        elif action == "remove":
            item.delete()
        return redirect("cart_detail")

class ClearCartView(View):
    def post(self, request):
        customer = _get_guest(request)
        order = get_or_create_order(request, customer)
        order.items.all().delete()
        return redirect("cart_detail")

class CartDetailView(View):
    def get(self, request):
        customer = _get_guest(request)
        order = get_or_create_order(request, customer)
        items = order.items.select_related("product", "product__category")
        rows = [{"item": it, "subtotal": it.product.price * it.quantity} for it in items]
        subtotal = sum(r["subtotal"] for r in rows)

        delivery = request.session.get("delivery")
        delivery_price = int(delivery["price"]) if delivery else 0
        total_price = subtotal + delivery_price

        return render(request, "cart_detail.html", {
            "order": order, "rows": rows,
            "subtotal": subtotal,
            "delivery": delivery,
            "total_price": total_price,
        })


SHIPPING_PRICES = {
    "nova_poshta": 99,
    "ukrposhta": 59,
    "meest": 79,
}

class DeliveryView(View):
    template_name = "delivery.html"

    def get(self, request):
        delivery = request.session.get("delivery") or {
            "method": "nova_poshta",
            "city": "",
            "department": "",
            "price": SHIPPING_PRICES["nova_poshta"],
        }
        return render(request, self.template_name, {
            "delivery": delivery,
            "prices": SHIPPING_PRICES,
        })

    def post(self, request):
        method = request.POST.get("method") or "nova_poshta"
        city = (request.POST.get("city") or "").strip()
        department = (request.POST.get("department") or "").strip()
        price = SHIPPING_PRICES.get(method, SHIPPING_PRICES["nova_poshta"])
        request.session["delivery"] = {
            "method": method,
            "city": city,
            "department": department,
            "price": price,
        }
        request.session.modified = True
        return redirect("cart_detail")


class AboutView(View):
    def get(self, request):
        return render(request, "about.html")
