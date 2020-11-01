from rest_framework.routers import SimpleRouter

from posts.views.post import PostViewSet

router = SimpleRouter()
router.register('posts', PostViewSet)


urlpatterns = router.urls
