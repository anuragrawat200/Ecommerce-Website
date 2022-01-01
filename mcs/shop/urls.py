from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="about"),
    # path("", views.contact, name="contact"),
    path("tracker/", views.tracker, name="tracker"),
    path("search/", views.search, name="Search"),
    path("checkout/", views.checkout, name="checkout"),
    path("demo<str:myid>", views.demo, name="demo"),
    path("products<int:myid>", views.productview, name="ProductView"),
    path("signup/", views.handleSignUp, name="handleSignUp"),
    path("login/", views.handelLogin, name="handleLogin"),
    path("logout/", views.handelLogout, name="handleLogout"),
    path("order/", views.handleorders, name="handleorders"),

]
