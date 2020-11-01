from django.db.models import Q
from django_filters import rest_framework as filters

from users.models import UserProxy


class UserFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_name')
    following_user = filters.NumberFilter(method='filter_following_user')
    followed_by_user = filters.NumberFilter(method='filter_followed_by_user')

    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value))

    def filter_following_user(self, queryset, name, user):
        # list users following user
        return queryset.filter(followings=user)

    def filter_followed_by_user(self, queryset, name, user):
        # list users followed by user
        return queryset.filter(followers=user)

    class Meta:
        model = UserProxy
        fields = ['name', 'following_user', 'followed_by_user']
