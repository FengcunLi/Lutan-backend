from rest_framework import generics, viewsets

from categories.models import Category
from categories.serializers import CategorySerializer, CategoryTreeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryTreeView(generics.RetrieveAPIView):
    serializer_class = CategoryTreeSerializer
    queryset = Category.objects.all()

    def get_object(self):
        root = super().get_object()
        descendants = root.get_descendants(include_self=True).order_by("lft")

        categories = {}
        for category in descendants:
            category.subcategories = []
            categories[category.id] = category
            if category.id != root.id and category.parent_id:
                categories[category.parent_id].subcategories.append(category)

        return categories[root.id]
