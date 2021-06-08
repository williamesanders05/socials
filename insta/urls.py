from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name = "create"),
    path("user<str:username>", views.account, name="account"),
    path("<int:post_id>/like", views.like, name="like"),
    path("saved", views.saved, name="saved")
]