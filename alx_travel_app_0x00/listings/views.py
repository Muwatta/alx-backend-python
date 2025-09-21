from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Listing
from .serializers import ListingSerializer


class ListingListView(generics.ListAPIView):
    """API endpoint to list all active travel listings."""
    queryset = Listing.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]