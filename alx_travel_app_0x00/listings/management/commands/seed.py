#!/usr/bin/env python3
"""Database seeding command for travel app."""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import timedelta, date
import random
from ...models import Listing, Booking, Review


User = get_user_model()


class Command(BaseCommand):
    """Seed travel app database with sample data."""
    
    help = 'Populate database with sample travel listings and bookings'
    
    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=6, help='Number of users')
        parser.add_argument('--listings', type=int, default=12, help='Number of listings')
        parser.add_argument('--bookings', type=int, default=15, help='Number of bookings')
        parser.add_argument('--reviews', type=int, default=10, help='Number of reviews')
    
    def handle(self, *args, **options):
        """Execute seeding."""
        self.stdout.write('Starting database seeding...')
        
        # Clear existing data
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Create data
        users = self._create_users(options['users'])
        listings = self._create_listings(options['listings'], users)
        bookings = self._create_bookings(options['bookings'], listings, users)
        reviews = self._create_reviews(options['reviews'], listings, users)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Seeding complete! {len(users)} users, {len(listings)} listings, '
                f'{len(bookings)} bookings, {len(reviews)} reviews created!'
            )
        )
    
    def _create_users(self, count):
        """Create users (hosts and guests)."""
        users = []
        
        # Hosts
        hosts = [
            {'username': 'sarah_h', 'email': 'sarah@travel.com', 'first': 'Sarah', 'last': 'Host'},
            {'username': 'mike_h', 'email': 'mike@travel.com', 'first': 'Mike', 'last': 'Landlord'},
        ]
        
        for data in hosts:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                first_name=data['first'],
                last_name=data['last'],
                password='pass123'
            )
            users.append(user)
        
        # Guests
        guest_first = ['Alice', 'Bob', 'Carol', 'David', 'Emma']
        guest_last = ['Guest', 'Traveler', 'Visitor', 'Explorer']
        
        for i in range(count - 2):
            user = User.objects.create_user(
                username=f'guest{i}',
                email=f'guest{i}@travel.com',
                first_name=guest_first[i % len(guest_first)],
                last_name=guest_last[i % len(guest_last)],
                password='pass123'
            )
            users.append(user)
        
        self.stdout.write(f'Created {len(users)} users')
        return users
    
    def _create_listings(self, count, users):
        """Create property listings."""
        listings = []
        hosts = [u for u in users if u.email.endswith('@travel.com')]
        
        cities = ['New York', 'Los Angeles', 'Miami', 'Austin', 'Seattle']
        types = ['apartment', 'house', 'room']
        
        for i in range(count):
            listing = Listing.objects.create(
                title=f"Cozy {random.choice(types)} in {random.choice(cities)}",
                description=f"Beautiful {random.choice(types)} with modern amenities.",
                address=f"{random.randint(100, 999)} {random.choice(['St', 'Ave', 'Blvd'])}",
                city=random.choice(cities),
                price_per_night=Decimal(random.uniform(80, 300)),
                max_guests=random.randint(2, 4),
                bedrooms=random.randint(1, 2),
                host=random.choice(hosts) if hosts else users[0],
                property_type=random.choice(types)
            )
            listings.append(listing)
            
            if i % 3 == 0:
                self.stdout.write(f'Created {i+1}/{count} listings...')
        
        self.stdout.write(f'Created {len(listings)} listings')
        return listings
    
    def _create_bookings(self, count, listings, users):
        """Create bookings."""
        guests = [u for u in users if not u.email.endswith('@travel.com')]
        
        for i in range(count):
            listing = random.choice(listings)
            guest = random.choice(guests) if guests else users[0]
            
            start = date.today() + timedelta(days=random.randint(10, 60))
            end = start + timedelta(days=random.randint(2, 5))
            nights = (end - start).days
            total = listing.price_per_night * Decimal(nights)
            
            Booking.objects.create(
                listing=listing,
                guest=guest,
                check_in_date=start,
                check_out_date=end,
                total_price=total,
                status=random.choice(['pending', 'confirmed'])
            )
            
            if i % 5 == 0:
                self.stdout.write(f'Created {i+1}/{count} bookings...')
    
    def _create_reviews(self, count, listings, users):
        """Create reviews."""
        reviewers = list(users)
        
        for i in range(count):
            listing = random.choice(listings)
            reviewer = random.choice([u for u in reviewers if u != listing.host])
            
            Review.objects.create(
                listing=listing,
                reviewer=reviewer,
                rating=random.randint(1, 5),
                title=f"Great stay in {listing.city}!",
                comment=f"Really enjoyed {listing.title}. Clean and comfortable.",
                stay_date=date.today() - timedelta(days=random.randint(1, 30))
            )
            
            if i % 3 == 0:
                self.stdout.write(f'Created {i+1}/{count} reviews...')