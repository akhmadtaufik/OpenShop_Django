from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "sku",
            "description",
            "shop",
            "location",
            "price",
            "discount",
            "category",
            "stock",
            "is_available",
            "picture",
            "is_delete",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "is_delete": {"write_only": True},
        }
