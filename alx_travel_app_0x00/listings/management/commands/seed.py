#!/usr/bin/env python3
"""Management command to seed travel app database - Robust version."""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import timedelta, date
import random
from ...models import Listing, Booking, Review


User = get_user_model()


class Command(BaseCommand):
    """Command to populate database with sample travel data."""
    
    help = 'Seed the database with sample travel listings, bookings, and reviews'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--users', type=int, default=6,
            help='Number of users to create (default: 6)'
        )
        parser.add_argument(
            '--listings', type=int, default=12,
            help='Number of listings to create (default: 12)'
        )
        parser.add_argument(
            '--bookings', type=int, default=15,
            help='Number of bookings to create (default: 15)'
        )
        parser.add_argument(
            '--reviews', type=int, default=10,
            help='Number of reviews to create (default: 10)'
        )
    
    def handle(self, *args, **options):
        """Execute the seeding process."""
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
                f'Seeding complete! Created {len(users)} users, '
                f'{len(listings)} listings, {len(bookings)} bookings, '
                f'{len(reviews)} reviews created!'
            )
        )


    def _create_users(self, count):
        """Create sample users (hosts and guests)."""
        users = []
        
        # Create 2-3 hosts first
        host_data = [
            {'username': 'sarah_host', 'email': 'sarah@travelapp.com', 'first_name': 'Sarah', 'last_name': 'Johnson'},
            {'username': 'mike_host', 'email': 'mike@travelapp.com', 'first_name': 'Mike', 'last_name': 'Williams'},
            {'username': 'emma_host', 'email': 'emma@travelapp.com', 'first_name': 'Emma', 'last_name': 'Davis'},
        ]
        
        num_hosts = min(3, count // 2)  # At least 2 hosts, but not more than half
        for i in range(num_hosts):
            try:
                user = User.objects.create_user(
                    username=host_data[i]['username'],
                    email=host_data[i]['email'],
                    first_name=host_data[i]['first_name'],
                    last_name=host_data[i]['last_name'],
                    password='password123'
                )
                users.append(user)
                self.stdout.write(f'Created host: {user.email}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create host {i+1}: {e}'))
        
        # Create remaining as guests
        num_guests = count - len(users)
        guest_names = [
            ('Alice', 'Wonder'), ('Bob', 'Builder'), ('Carol', 'Davis'),
            ('David', 'Evans'), ('Emma', 'Foster'), ('Frank', 'Green'),
            ('Grace', 'Harris'), ('Henry', 'Irving'), ('Ivy', 'Jackson'),
            ('Jack', 'King'), ('Kelly', 'Lewis'), ('Liam', 'Miller')
        ]
        
        for i in range(num_guests):
            try:
                first, last = guest_names[i % len(guest_names)]
                user = User.objects.create_user(
                    username=f'guest{i+1}',
                    email=f'guest{i+1}@travelapp.com',
                    first_name=first,
                    last_name=last,
                    password='password123'
                )
                users.append(user)
                if (i + 1) % 2 == 0:
                    self.stdout.write(f'Created guest {i+1}: {user.email}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create guest {i+1}: {e}'))
        
        self.stdout.write(f'Created {len(users)} total users ({len([u for u in users if u.username.startswith("host")])} hosts)')
        return users


    def _create_listings(self, count, users):
        """Create sample property listings."""
        listings = []
        
        # Get host users (users with 'host' in username)
        host_users = [u for u in users if u.username.startswith('host')]
        
        # Fallback if no hosts
        if not host_users:
            self.stdout.write(self.style.WARNING('No host users found - using first user as host'))
            host_users = [users[0]] if users else []
        
        if not host_users:
            self.stdout.write(self.style.ERROR('Cannot create listings - no users available'))
            return listings  # Return empty list
        
        cities = ['New York', 'Los Angeles', 'Miami', 'Austin', 'Seattle', 'Denver', 'Chicago', 'Boston']
        property_types = ['apartment', 'house', 'room', 'villa']
        adjectives = ['Cozy', 'Modern', 'Luxury', 'Downtown', 'Beachfront', 'City Center']
        
        for i in range(count):
            try:
                listing = Listing.objects.create(
                    title=f"{random.choice(adjectives)} {random.choice(property_types).title()} in {random.choice(cities)}",
                    description=f"Beautiful {random.choice(property_types)} with modern amenities and great location in {random.choice(cities)}. Perfect for your next vacation!",
                    address=f"{random.randint(100, 9999)} {random.choice(['Main St', 'Oak Ave', 'Pine Rd', 'Elm Blvd', 'Cedar Ln'])}",
                    city=random.choice(cities),
                    country='USA',
                    price_per_night=Decimal(random.uniform(65, 420)).quantize(Decimal('0.01')),
                    max_guests=random.randint(1, 6),
                    bedrooms=random.randint(1, 4),
                    beds=random.randint(1, 5),
                    baths=Decimal(random.choice([1.0, 1.5, 2.0, 2.5, 3.0])),
                    property_type=random.choice(property_types),
                    host=random.choice(host_users),
                    is_active=True
                )
                listings.append(listing)
                
                if (i + 1) % 3 == 0:
                    self.stdout.write(f'Created {i+1}/{count} listings...')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create listing {i+1}: {e}'))
        
        self.stdout.write(f'Created {len(listings)} listings')
        return listings


    def _create_bookings(self, count, listings, users):
        """Create sample bookings."""
        if not listings or not users:
            self.stdout.write(self.style.WARNING('Skipping bookings - insufficient data'))
            return []  # Return empty list
        
        # Get guest users (exclude hosts)
        guest_users = [u for u in users if not u.username.startswith('host')]
        if not guest_users:
            guest_users = users  # Fallback to all users
        
        bookings = []  # Initialize empty list
        
        for i in range(count):
            try:
                listing = random.choice(listings)
                guest = random.choice(guest_users)
                
                # Generate random future dates
                start_date = date.today() + timedelta(days=random.randint(7, 120))
                end_date = start_date + timedelta(days=random.randint(1, 7))
                nights = (end_date - start_date).days
                total_price = listing.price_per_night * Decimal(nights)
                
                booking = Booking.objects.create(
                    listing=listing,
                    guest=guest,
                    check_in_date=start_date,
                    check_out_date=end_date,
                    number_of_guests=random.randint(1, min(3, listing.max_guests)),
                    total_price=total_price,
                    status=random.choice(['pending', 'confirmed', 'cancelled'])
                )
                bookings.append(booking)  # Add to list
                
                if (i + 1) % 5 == 0:
                    self.stdout.write(f'Created {i+1}/{count} bookings...')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create booking {i+1}: {e}'))
        
        self.stdout.write(f'Created {len(bookings)} bookings')
        return bookings  # Return the list


    def _create_reviews(self, count, listings, users):
        """Create sample reviews."""
        if not listings or not users:
            self.stdout.write(self.style.WARNING('Skipping reviews - insufficient data'))
            return []  # Return empty list
        
        # Get reviewer users (anyone except listing hosts)
        reviewer_users = list(users)
        
        review_templates = [
            "Amazing stay! The {city} location was perfect.",
            "Great property and host. Highly recommended!",
            "Clean, comfortable, and exactly as described.",
            "Fantastic experience! Would definitely return.",
            "Excellent {property_type} in a great neighborhood."
        ]
        
        reviews = []  # Initialize empty list
        
        for i in range(count):
            try:
                listing = random.choice(listings)
                reviewer = random.choice(reviewer_users)
                
                # Skip if reviewer is the host
                if reviewer == listing.host:
                    continue
                
                review_text = random.choice(review_templates).format(
                    city=listing.city,
                    property_type=listing.property_type
                )
                
                review = Review.objects.create(
                    listing=listing,
                    reviewer=reviewer,
                    rating=random.randint(3, 5),  # Mostly positive
                    title=f"{random.choice(['Great', 'Amazing', 'Fantastic'])} {listing.city} Stay",
                    comment=f"{review_text} The host was very responsive and the {listing.property_type} was clean and comfortable.",
                    stay_date=date.today() - timedelta(days=random.randint(30, 365))
                )
                reviews.append(review)  # Add to list
                
                if (i + 1) % 3 == 0:
                    self.stdout.write(f'Created {i+1}/{count} reviews...')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create review {i+1}: {e}'))
        
        self.stdout.write(f'Created {len(reviews)} reviews')
        return reviews  # Return the list