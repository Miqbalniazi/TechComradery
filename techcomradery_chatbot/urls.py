from django.urls import path
from .views import home, login, get_response, save_response, display


urlpatterns = [
    path("", login, name="login"),
    path("home/", home, name="home"),
    path("request/", get_response, name="request"),
    path("response/", save_response, name="response"),
    path("display/<user_id>/", display, name="display"),
]