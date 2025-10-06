from django.contrib import admin
from django.urls import path, include
from messaging_app.chats import auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(auth.urlpatterns)),
]
