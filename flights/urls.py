from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("flight/<str:id>", views.flight_view, name="flight"),
    path("code/<str:code>", views.airport_view, name="airport"),
    path("airports/", views.all_airports, name="airports"),
    path("book/<str:id>", views.book, name="book"),
    path("cancel/<str:id>", views.cancel_book, name="cancel"),
    path("myflights", views.my_flights, name="myflights")
]
