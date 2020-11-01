from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from categories.models import Category


# With object permissions support
class CategoryAdmin(GuardedModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
