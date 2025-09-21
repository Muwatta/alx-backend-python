#!/usr/bin/env python3
"""Messaging app models."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid


class CustomUserManager(BaseUserManager):
    """Custom manager for User model - uses email instead of username."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with email."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with email."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with messaging features."""
    
    # Use custom manager
    objects = CustomUserManager()
    
    # Role choices (lowercase for consistency)
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    
    # UUID primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Required fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    
    # Optional fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Email as username
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # Fix group/permission conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    class Meta:
        indexes = [models.Index(fields=['email'])]
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"


class Conversation(models.Model):
    """Conversation between multiple users."""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Simple many-to-many (no through model)
    participants = models.ManyToManyField(
        User,
        related_name='conversations'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['created_at'])]
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
    
    def __str__(self):
        return f"Conversation {self.id} ({self.participants.count()} participants)"


class Message(models.Model):
    """Individual message in a conversation."""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['conversation', 'sent_at']),
            models.Index(fields=['sender', 'sent_at']),
        ]
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
    
    def __str__(self):
        return f"{self.sender} in {self.conversation.id}: {self.message_body[:30]}"
    