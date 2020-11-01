from django.urls import path
from rest_framework_nested.routers import SimpleRouter

from categories.views import CategoryTreeView, CategoryViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet)

urlpatterns = router.urls + [
    path('categories/tree/<int:pk>', CategoryTreeView.as_view())
]
