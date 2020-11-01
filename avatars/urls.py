from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

from avatars.views import AvatarViewSet

router = SimpleRouter()

router.register('avatars', AvatarViewSet)

# Return a URL pattern for serving files in debug mode.
urlpatterns = router.urls + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
