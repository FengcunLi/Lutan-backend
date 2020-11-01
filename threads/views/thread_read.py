from rest_framework import mixins, viewsets

from threads.models.thread_read import ThreadRead
from threads.serializers.thread_read import ThreadReadSerializer


class ThreadReadViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = ThreadReadSerializer
    queryset = ThreadRead.objects.all()
