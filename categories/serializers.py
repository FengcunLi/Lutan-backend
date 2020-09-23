from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from categories.models import Category


class CategoryTreeSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    subcategories = serializers.ListSerializer(read_only=True,
                                               child=RecursiveField())

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


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    level = serializers.IntegerField(read_only=True)
    lft = serializers.IntegerField(read_only=True)
    rght = serializers.IntegerField(read_only=True)

    is_leaf_node = serializers.SerializerMethodField()
    is_child_node = serializers.SerializerMethodField()
    is_root_node = serializers.SerializerMethodField()

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
            "is_leaf_node",
            "is_child_node",
            "is_root_node"
        ]

    def get_is_leaf_node(self, obj):
        return obj.is_leaf_node()

    def get_is_child_node(self, obj):
        return obj.is_child_node()

    def get_is_root_node(self, obj):
        return obj.is_root_node()
