from django_filters import rest_framework as filters
from django_filters.filters import DateTimeFromToRangeFilter
from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = DateTimeFromToRangeFilter(field_name='created_at')
    status = filters.CharFilter(field_name='status')
    creator = filters.NumberFilter(field_name='creator__id')

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status', 'creator']
