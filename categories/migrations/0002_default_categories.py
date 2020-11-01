from django.db import migrations

from categories import PUBLIC_THREADS_CATEGORY_TREE_ROOT_NAME


def create_default_categories(apps, schema_editor):
    # Category = apps.get_model("categories", "Category")
    from categories.models import Category

    root = Category.objects.create(
        name=PUBLIC_THREADS_CATEGORY_TREE_ROOT_NAME,
        level=0,
    )


class Migration(migrations.Migration):

    dependencies = [("categories", "0001_initial")]

    operations = [migrations.RunPython(create_default_categories)]
