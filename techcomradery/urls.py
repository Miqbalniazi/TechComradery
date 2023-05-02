from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("techcomradery_client.urls")),
    path("chatbot/", include("techcomradery_chatbot.urls")),
]
