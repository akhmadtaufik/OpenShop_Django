from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProductSerializer


class ProductList(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        product = serializer.save()
        product_id = str(product.id)
        data = serializer.data
        response_body = {
            "id": data["id"],
            "name": data["name"],
            "shop": data["shop"],
            "price": data["price"],
            "sku": data["sku"],
            "description": data["description"],
            "location": data["location"],
            "discount": data["discount"],
            "category": data["category"],
            "stock": data["stock"],
            "is_available": data["is_available"],
            "picture": data["picture"],
            "_links": [
                {
                    "rel": "self",
                    "href": "/products",
                    "action": "POST",
                    "types": ["application/json"],
                },
                {
                    "rel": "self",
                    "href": f"/products/{product_id}/",
                    "action": "GET",
                    "types": ["application/json"],
                },
                {
                    "rel": "self",
                    "href": f"/products/{product_id}/",
                    "action": "PUT",
                    "types": ["application/json"],
                },
                {
                    "rel": "self",
                    "href": f"/products/{product_id}/",
                    "action": "DELETE",
                    "types": ["application/json"],
                },
            ],
        }
        return Response(response_body, status=status.HTTP_201_CREATED)
