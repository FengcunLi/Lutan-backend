import django_filters
from djoser import views
from rest_framework import filters, permissions
from rest_framework.pagination import PageNumberPagination

from users.filters import UserFilter
from users.models import UserProxy


class UserPaginationClass(PageNumberPagination):
    # default page size
    page_size = 100

    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserViewSet(views.UserViewSet):
    pagination_class = UserPaginationClass
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = UserFilter
    ordering_fields = ['id', 'first_name']
    ordering = ['id']

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = [permissions.AllowAny, ]
        return super().get_permissions()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            return UserProxy.objects.none()

        # django-guardian's migration will insert one anonymous user with email = AnonymousUser
        queryset = super().get_queryset().exclude(email='AnonymousUser')
        if self.action in ['me', 'list']:
            queryset = queryset.prefetch_related('posts')\
                .prefetch_related('threads')\
                .prefetch_related('followers')\
                .prefetch_related('avatars')
        return queryset
