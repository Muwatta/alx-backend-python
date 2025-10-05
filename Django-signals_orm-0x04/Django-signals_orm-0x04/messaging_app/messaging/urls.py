from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('delete-account/', views.delete_user, name='delete_user'),
    path('messages/<int:receiver_id>/', views.message_list, name='message_list'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]