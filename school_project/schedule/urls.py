from django.urls import path
from schedule.views import ProductListView
urlpatterns = [
    path('products/',ProductListView.as_view(),name='product-list')
]


