from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from categories.models import Category
from categories.serializers import (CategoryCreateSerializer,
                                    CategoryTreeSerializer)


class CategoryViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = CategoryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        serializer = CategoryCreateSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def tree(self, request, pk=None):
        root = Category.objects.get(pk=pk)
        queryset = root.get_descendants(include_self=True).order_by("lft")

        categories = {}
        for category in queryset:
            category.subcategories = []
            categories[category.id] = category
            if category.id != root.id and category.parent_id:
                categories[category.parent_id].subcategories.append(category)

        serializer = CategoryTreeSerializer(
            categories[root.id], context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
