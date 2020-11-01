from django_filters import rest_framework as filters

from threads.models import Thread


class ThreadFilter(filters.FilterSet):
    title = filters.CharFilter(method='filter_title')
    categories = filters.CharFilter(method='filter_categories')
    starter = filters.CharFilter(method='filter_starter')

    def filter_title(self, queryset, name, value):
        return queryset.filter(title_search_vector=value)

    def filter_categories(self, queryset, name, value):
        categories = value.split(",")
        categories_clean = []
        for category in categories:
            try:
                categories_clean.append(int(category))
            except:
                pass
        return queryset.filter(category__in=categories_clean)

    def filter_starter(self, queryset, name, value):
        return queryset.filter(starter=value)

    class Meta:
        model = Thread
        fields = ['title', 'categories', 'starter']
