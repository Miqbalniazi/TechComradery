from django.urls import path
from .views import register, is_user_exists, subscribe


urlpatterns = [
    path("register/", register, name="register"),
    path("check/", is_user_exists, name="check"),
    path("subscribe/", subscribe, name="check"),
]