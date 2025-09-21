#!/usr/bin/env python3
"""Travel booking models for listings, bookings, and reviews."""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid


class Listing(models.Model):
    """Property listing for vacation rentals."""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Property details
    title = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='USA')
    
    # Pricing & capacity
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    max_guests = models.PositiveIntegerField(default=2)
    bedrooms = models.PositiveIntegerField(default=1)
    beds = models.PositiveIntegerField(default=1)
    baths = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    
    # Property type
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('private_room', 'Private Room'),
        ('villa', 'Villa'),
        ('cottage', 'Cottage'),
    ]
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES,
        default='apartment'
    )
    
    # Location coordinates (optional)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Host relationship
    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='hosted_listings'
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'created_at']),
            models.Index(fields=['property_type']),
            models.Index(fields=['price_per_night']),
            models.Index(fields=['city']),
            models.Index(fields=['host']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.city}"


class Booking(models.Model):
    """Reservation for a property stay."""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Relationships
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    guest = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='made_bookings'
    )
    
    # Dates
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    
    # Details
    number_of_guests = models.PositiveIntegerField(default=1)
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Pricing
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['listing', 'check_in_date']),
            models.Index(fields=['guest', 'status']),
            models.Index(fields=['status', 'check_in_date']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(check_out_date__gt=models.F('check_in_date')),
                name='valid_dates'
            )
        ]
    
    def save(self, *args, **kwargs):
        """Auto-calculate total price if not set."""
        if not self.total_price:
            nights = (self.check_out_date - self.check_in_date).days
            self.total_price = self.listing.price_per_night * nights
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.guest.username} books {self.listing.title}"


class Review(models.Model):
    """Guest review after stay."""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Relationships
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='written_reviews'
    )
    
    # Content
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=100)
    comment = models.TextField()
    
    # Stay reference
    stay_date = models.DateField(null=True, blank=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['listing', 'created_at']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.reviewer.username}: {self.rating}/5 - {self.listing.title}"