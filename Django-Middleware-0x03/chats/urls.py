from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatView.as_view(), name='chat'),
    path('admin-action/', views.AdminActionView.as_view(), name='admin_action'),
]
