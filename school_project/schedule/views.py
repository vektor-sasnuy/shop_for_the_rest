from django.views import View
from django.urls import reverse
from schedule.models import Product,Order
from django.http import JsonResponse
from django.shortcuts import render, redirect


class HomePageView(View):
    def get(self, request):
        products = Product.objects.all()[:8]  # Показати лише перші 8 товарів
        return render(request, 'home.html', {
            'products': products,
            'show_catalog_btn': True,
        })


class ProductListView(View):

    def get(self,request):
        products = Product.objects.all()
        return render(request,'products_list.html',{'products':products})
    

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)  # Fetch product by ID
            return render(request, 'product_detail.html', {'product': product})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)