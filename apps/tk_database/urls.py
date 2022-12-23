from django.urls import path
from apps.tk_database import views

urlpatterns = [
    path("", views.hike_index, name="hike_index"),
    path("hike/<int:pk>/", views.hike_detail, name="hike_detail"),
    path("hike/<int:pk>/edit", views.hike_detail, name="hike_edit"),
    path("hike/new", views.hike_new, name="hike_new"),
]