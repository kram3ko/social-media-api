from django_filters import rest_framework as filters


class PostFilter(filters.FilterSet):
    post = filters.CharFilter(lookup_expr="icontains")
    created_at = filters.DateFromToRangeFilter()
