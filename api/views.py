from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from main.models import CategoryModel, ItemModel, LinkModel


class CategoryApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            title = request.data.get("title")
            CategoryModel.objects.get_or_create(title__iexact=title)
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
            title = request.data.get("title")
            category_title = request.data.get("category")
            category, created = CategoryModel.objects.get_or_create(
                title__iexact=category_title,
                defaults={"title": category_title}
            )
            ItemModel.objects.get_or_create(
                title=title,
                category=category,
                defaults={"title": title, "category": category}
            )
            return Response(
                {"message": "Item created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
