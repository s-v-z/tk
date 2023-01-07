from django.urls import path
from django.views.generic.base import TemplateView
from apps.tk_database import views


urlpatterns = [
    path("", views.tk_home, name="tk_home"),

    path("user/list", views.users_list, name="users_list"),
    path("user/<int:user_id>/show", views.user_show, name="user_show"),
    path("user/<int:user_id>/announcements", views.user_announcements, name="user_announcements"),
    path("user/<int:user_id>/hikes", views.user_hikes, name="user_hikes"),

    path("hike/list", views.hikes_list, name="hikes_list"),
    path("hike/new", views.CreateHikeView.as_view(), name="hike_new"),
    path("hike/<int:hike_id>/", views.hike_show, name="hike_show"),
    path("hike/<int:hike_id>/edit", views.UpdateHikeView.as_view(), name="hike_edit"),
    path("hike/<int:hike_id>/delete", views.DeleteHikeView.as_view(), name="hike_delete"),
    path("hike/<int:hike_id>/close", views.hike_close, name="hike_close"),


    path("hike/report/list", views.reports_list, name="reports_list"),
    path("hike/<int:hike_id>/report/new", views.CreateReportView.as_view(), name="report_new"),
    path("hike/<int:hike_id>/report/", views.report_show, name="report_show"),
    path("hike/<int:hike_id>/report/edit", views.report_edit, name="report_edit"),
    path("hike/<int:hike_id>/report/delete", views.report_edit, name="report_delete"),

    path("report/list", views.reports_list, name="reports_list"),
    path("event/list", views.events_list, name="events_list"),
    
    path("about/club", TemplateView.as_view(template_name='about/club.html'), name="about_club"),
    path("about/training", TemplateView.as_view(template_name='about/training.html'), name="about_training"),
]
