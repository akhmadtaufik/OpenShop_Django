from django.urls import path

from .views import ProductDetail, ProductList

urlpatterns = [
    path("", ProductList.as_view(), name="product-list"),
    path("<str:product_id>/", ProductDetail.as_view(), name="product-detail"),
]
