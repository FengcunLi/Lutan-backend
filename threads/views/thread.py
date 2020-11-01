import django_filters
from django.contrib.auth import get_user_model
from django.db.models.expressions import F
from django.db.models.functions import Greatest
from django.db.models.query import Prefetch
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from permissions.thread import (CanChangeThisThread,
                                CanChangeThreadInThisCategory,
                                CanDeleteThisThread,
                                CanDeleteThreadInThisCategory,
                                CanStartThreadInThisCategory, IsStarter)
from posts.models.post import Post
from threads.filters import ThreadFilter
from threads.models.thread import Thread
from threads.serializers.thread import (ThreadListSerializer,
                                        ThreadRetrieveSerializer,
                                        ThreadWritableSerializer)
from users.permissions import IsAdmin, IsGeneralUser

UserModel = get_user_model()


class ThreadPaginationClass(PageNumberPagination):
    # default page size
    page_size = 100

    page_size_query_param = 'page_size'
    max_page_size = 1000


class ThreadViewSet(viewsets.ModelViewSet):
    pagination_class = ThreadPaginationClass
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = ThreadFilter
    # override get_serializer_class to switch the serializer class according to action.
    # It's not recommended to use different serializer class in different action method directly.
    # because the swagger may not work properly when generating schema.
    # https://github.com/encode/django-rest-framework/issues/4545#issuecomment-252343839

    def get_serializer_class(self):
        if self.action in ["create", "partial_update", "update"]:
            return ThreadWritableSerializer
        elif self.action == "retrieve":
            return ThreadRetrieveSerializer
        else:
            return ThreadListSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated,
                                       IsAdmin | IsGeneralUser | CanStartThreadInThisCategory]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated,
                                       IsAdmin | IsStarter | CanDeleteThreadInThisCategory | CanDeleteThisThread]
        elif self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated,
                                       IsAdmin | IsStarter | CanChangeThreadInThisCategory | CanChangeThisThread]
        elif self.action == 'retrieve':
            self.permission_classes = [AllowAny]
        elif self.action == 'list':
            self.permission_classes = [AllowAny]
        elif self.action == 'my':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    # Used in actions: retrieve, update, destory.
    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            return Thread.objects.none()

        # prefetch_poster = Prefetch("poster",
        #                            queryset=UserModel.objects.prefetch_related('avatars'))
        prefetch_posts = Prefetch("posts",
                                  queryset=(Post.objects.filter(parent__isnull=True)
                                            .order_by('created_on')
                                            .prefetch_related("post_likes")
                                            .select_related("poster"))
                                  )
        # prefetch_starter = Prefetch("starter",
        #                             queryset=UserModel.objects.prefetch_related('avatars'))
        return Thread.objects.all().prefetch_related(prefetch_posts).select_related('starter')

    def get_ordered_queryset(self):
        queryset = self.get_queryset()

        # Greatest: If any expression is null the return value is database-specific: On PostgreSQL,
        # the maximum not-null expression is returned.
        # On MySQL, Oracle, and SQLite, if any expression is null, null is returned.
        # queryset = (
        #     queryset
        #     .annotate(latest_posted=Max("posts__created_on"))
        #     .annotate(latest=Greatest("latest_posted", "created_on"))
        #     .order_by("-latest")
        # )
        queryset = (
            queryset
            .annotate(latest=Greatest("last_post_created_on", "created_on"))
            .order_by("-latest")
        )
        return queryset

    def list(self, request):
        queryset = self.get_ordered_queryset()
        return self.build_response(queryset)

    @action(
        methods=["get"],
        detail=False,
        url_path="my",
        url_name="my-threads",
    )
    def my(self, request):
        user = request.user
        queryset = self.get_ordered_queryset()
        queryset = queryset.filter(starter=user)
        return self.build_response(queryset)

    @action(
        methods=["get"],
        detail=False,
        url_path="subscribed",
        url_name="subscribed-threads",
        permission_classes=[IsAuthenticated],
    )
    def subscribed(self, request):
        user = request.user
        queryset = self.get_ordered_queryset()
        subscribed_threads = user.thread_subscription.values("thread_id")
        queryset = queryset.filter(id__in=subscribed_threads)
        return self.build_response(queryset)

    @action(
        methods=["get"],
        detail=False,
        url_path="unapproved",
        url_name="unapproved-threads",
        permission_classes=[IsAuthenticated],
    )
    def unapproved(self, request):
        queryset = self.get_ordered_queryset().filter(is_unapproved=True)
        return self.build_response(queryset)

    @action(
        methods=["get"],
        detail=False,
        url_path="new",
        url_name="new-threads",
        permission_classes=[IsAuthenticated],
    )
    def new(self, request):
        user = request.user
        queryset = self.get_ordered_queryset().exclude(thread_read__user=user)
        return self.build_response(queryset)

    # def has_unread_posts or def has_new_posts
    @action(
        methods=["get"],
        detail=False,
        url_path="has-new-posts",
        url_name="has-new-posts-threads",
        permission_classes=[IsAuthenticated],
    )
    def has_new_posts(self, request):
        user = request.user
        queryset = (
            self.get_ordered_queryset()
            .filter(thread_read__user=user)
            .exclude(thread_read__time__gt=F("latest_posted"))
        )
        return self.build_response(queryset)

    def build_response(self, queryset):
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def merge(self, other_thread):
    #     if self.pk == other_thread.pk:
    #         raise ValueError("thread can't be merged with itself")

    #     from ..signals import merge_thread

    #     merge_thread.send(sender=self, other_thread=other_thread)

    # def move(self, new_category):
    #     from ..signals import move_thread

    #     self.category = new_category
    #     move_thread.send(sender=self)
