from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from main.models import CategoryModel, ItemModel, LinkModel


class CategoryApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            category_title = request.data.get("category_title")
            CategoryModel.objects.get_or_create(title__iexact=category_title, defaults={"title": category_title})
            return Response(
                {"message": "Category created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ItemApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            category_title = request.data.get("category_title")
            item_title = request.data.get("item_title")
            category, created = CategoryModel.objects.get_or_create(
                title__iexact=category_title, defaults={"title": category_title}
            )
            ItemModel.objects.get_or_create(
                title=item_title,
                category=category,
                defaults={"title": item_title, "category": category},
            )
            return Response(
                {"message": "Item created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LinkApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            category_title = request.data.get("category_title")
            item_title = request.data.get("item_title")
            link_url = request.data.get("link_url")
            category, created = CategoryModel.objects.get_or_create(
                title__iexact=category_title, defaults={"title": category_title}
            )
            item, created = ItemModel.objects.get_or_create(
                title=item_title,
                category=category,
                defaults={"title": item_title, "category": category},
            )
            LinkModel.objects.get_or_create(
                url=link_url, item=item, defaults={"url": link_url, "item": item}
            )
            return Response(
                {"message": "Link created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
