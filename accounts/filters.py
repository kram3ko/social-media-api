from django_filters import rest_framework as filters


class UserProfileFilter(filters.FilterSet):
    username = filters.BaseInFilter(field_name="user__username", lookup_expr="in")
    user_info = filters.CharFilter(field_name="user__username", lookup_expr="icontains")
    created_at = filters.DateFromToRangeFilter(
        field_name="user__created_at", label="User Created At"
    )
