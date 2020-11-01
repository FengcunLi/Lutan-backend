from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet)
urls = router.urls

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.urls.authtoken')),
] + urls
