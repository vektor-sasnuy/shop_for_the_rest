from django.views import View
from schedule.models import Product,Order
from django.http import JsonResponse
from django.shortcuts import render


class ProductListView(View):
    def get(self,request):
        products = Product.objects.all()
        return render(request,'products_list.html',{'products':products})
    