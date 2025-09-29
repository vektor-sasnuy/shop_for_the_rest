from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:product_id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/add-to-cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path("cart/", views.CartDetailView.as_view(), name="cart_detail"),
    path("cart/item/<int:item_id>/", views.UpdateCartItemView.as_view(), name="cart_item_update"),
    path("cart/clear/", views.ClearCartView.as_view(), name="cart_clear"),
]
