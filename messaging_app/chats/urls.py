#!/usr/bin/env python3
"""URL configuration for chats API."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet


# Create router for automatic URL generation
router = DefaultRouter()

# Register with explicit basename
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    # API root - all endpoints
    path('api/', include(router.urls)),
]#!/usr/bin/env python3
"""URL configuration for chats API."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet


# Create router for automatic URL generation
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    # API root - all endpoints under /api/
    path('api/', include(router.urls)),
]