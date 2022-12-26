from django.urls import path
from apps.tk_database import views

urlpatterns = [
    path("", views.hikes_list, name="hikes_list"),
    path("user/<int:user_id>/announcements", views.user_announcements, name="user_announcements"),
    path("user/<int:user_id>/hikes", views.user_hikes, name="user_hikes"),
    path("hike/new", views.CreateHikeView.as_view(), name="hike_new"),
    path("hike/<int:hike_id>/", views.hike_show, name="hike_show"),
    path("hike/<int:hike_id>/edit", views.UpdateHikeView.as_view(), name="hike_edit"),
    path("hike/<int:hike_id>/delete", views.DeleteHikeView.as_view(), name="hike_delete"),
]