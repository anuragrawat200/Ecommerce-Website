from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="blogHome"),
    path("blogpost/blog<int:id>", views.blogpost, name="blogpostHome")
]
