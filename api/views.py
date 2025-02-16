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
