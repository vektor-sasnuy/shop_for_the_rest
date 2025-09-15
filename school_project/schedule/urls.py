from django.urls import path
from schedule.views import ProductListView, HomePageView, ProductDetailView, AddToCartView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
]
