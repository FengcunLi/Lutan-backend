from rest_framework import serializers

from categories.models import Category


class CategoryTreeSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "parent",
            "name",
            "description",
            "is_closed",
            "level",
            "lft",
            "rght",
            "subcategories"
        ]

    def get_subcategories(self, obj):
        if len(obj.subcategories) > 0:
            return self.__class__(obj.subcategories, many=True, context=self.context).data
        else:
            return []


class CategoryCreateSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    level = serializers.IntegerField(read_only=True)
    lft = serializers.IntegerField(read_only=True)
    rght = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "parent",
            "name",
            "description",
            "is_closed",
            "level",
            "lft",
            "rght",
        ]
