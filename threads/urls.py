from rest_framework.routers import SimpleRouter

from threads.views.thread import ThreadViewSet
from threads.views.thread_read import ThreadReadViewSet
from threads.views.thread_subscription import ThreadSubscriptionViewSet

router = SimpleRouter()
router.register('threads', ThreadViewSet, basename='thread')
router.register('thread-read', ThreadReadViewSet)
router.register('thread-subscription', ThreadSubscriptionViewSet)

urlpatterns = router.urls
