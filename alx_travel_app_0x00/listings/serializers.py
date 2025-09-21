#!/usr/bin/env python3
"""Serializers for travel listings API."""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Listing, Booking, Review


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Basic user info for API."""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    """Review with reviewer info."""
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'rating', 'title', 'comment',
            'reviewer', 'stay_date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    """Booking with guest and listing info."""
    guest = UserSerializer(read_only=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    listing_city = serializers.CharField(source='listing.city', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_title', 'listing_city',
            'guest', 'check_in_date', 'check_out_date',
            'number_of_guests', 'status', 'total_price',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'total_price']


class ListingSerializer(serializers.ModelSerializer):
    """Full listing with host, bookings, and reviews."""
    
    host = UserSerializer(read_only=True)
    bookings_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    recent_reviews = ReviewSerializer(many=True, read_only=True, source='reviews')
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'address', 'city', 'country',
            'price_per_night', 'max_guests', 'bedrooms', 'beds', 'baths',
            'property_type', 'latitude', 'longitude', 'is_active',
            'host', 'created_at', 'updated_at', 'bookings_count',
            'average_rating', 'recent_reviews'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_bookings_count(self, obj):
        """Count of bookings for this listing."""
        return obj.bookings.count()
    
    def get_average_rating(self, obj):
        """Average rating from reviews."""
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None