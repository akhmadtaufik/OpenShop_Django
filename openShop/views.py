from uuid import UUID

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


class ProductList(APIView):
    def _build_links(self, request, product_id):
        products_base_url = request.build_absolute_uri("/products")
        product_detail_url = request.build_absolute_uri(
            f"/products/{product_id}/"
        )
        return [
            {
                "rel": "self",
                "href": products_base_url,
                "action": "POST",
                "types": ["application/json"],
            },
            {
                "rel": "self",
                "href": product_detail_url,
                "action": "GET",
                "types": ["application/json"],
            },
            {
                "rel": "self",
                "href": product_detail_url,
                "action": "PUT",
                "types": ["application/json"],
            },
            {
                "rel": "self",
                "href": product_detail_url,
                "action": "DELETE",
                "types": ["application/json"],
            },
        ]

    def _build_product_response(self, request, data):
        product_id = data["id"]
        return {
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
            "_links": self._build_links(request, product_id),
        }

    def get(self, request):
        products = Product.objects.all()
        name_keyword = request.query_params.get("name")
        location_keyword = request.query_params.get("location")

        if name_keyword:
            products = products.filter(name__icontains=name_keyword)

        if location_keyword:
            products = products.filter(
                location__icontains=location_keyword
            )

        serializer = ProductSerializer(products, many=True)
        response_products = [
            self._build_product_response(request, item)
            for item in serializer.data
        ]
        return Response(
            {"products": response_products}, status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        response_body = self._build_product_response(request, serializer.data)
        return Response(response_body, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def _build_links(self, request, product_id):
        products_base_url = request.build_absolute_uri("/products")
        product_detail_url = request.build_absolute_uri(
            f"/products/{product_id}/"
        )
        return [
            {
                "rel": "self",
                "href": products_base_url,
                "action": "POST",
                "types": ["application/json"],
            },
            {
                "rel": "self",
                "href": product_detail_url,
                "action": "GET",
                "types": ["application/json"],
            },
            {
                "rel": "self",
                "href": product_detail_url,
                "action": "PUT",
                "types": ["application/json"],
            },
            {
                "rel": "self",
                "href": product_detail_url,
                "action": "DELETE",
                "types": ["application/json"],
            },
        ]

    def get(self, request, product_id):
        try:
            uuid_product_id = UUID(product_id)
        except ValueError:
            return Response(
                {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        product = Product.objects.filter(id=uuid_product_id).first()
        if not product:
            return Response(
                {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product)
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
            "is_delete": product.is_delete,
            "_links": self._build_links(request, data["id"]),
        }
        return Response(response_body, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        try:
            uuid_product_id = UUID(product_id)
        except ValueError:
            return Response(
                {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        product = Product.objects.filter(id=uuid_product_id).first()
        if not product:
            return Response(
                {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product, data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
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
            "is_delete": product.is_delete,
            "_links": self._build_links(request, data["id"]),
        }
        return Response(response_body, status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        try:
            uuid_product_id = UUID(product_id)
        except ValueError:
            return Response(
                {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        product = Product.objects.filter(id=uuid_product_id).first()
        if not product:
            return Response(
                {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        product.is_delete = True
        product.save(update_fields=["is_delete"])
        return Response(status=status.HTTP_204_NO_CONTENT)
