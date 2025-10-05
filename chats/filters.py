from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='conversation__participants__email')
    time_range = filters.DateTimeFromToRangeFilter(field_name='sent_at')

    class Meta:
        model = Message
        fields = ['user', 'time_range']
