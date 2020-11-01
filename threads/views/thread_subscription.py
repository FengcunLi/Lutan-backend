from rest_framework import mixins, viewsets

from threads.models.thread_subscription import ThreadSubscription
from threads.serializers.thread_subscription import \
    ThreadSubscriptionSerializer


class ThreadSubscriptionViewSet(mixins.CreateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    serializer_class = ThreadSubscriptionSerializer
    queryset = ThreadSubscription.objects.all()
