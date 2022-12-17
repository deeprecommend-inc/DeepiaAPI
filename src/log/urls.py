from django.urls import path
from log import views

urlpatterns = [
    path("", views.log_list, name="log-list"),
    path("<int:pk>/", views.log_detail, name="log-detail"),
    path("delete/", views.log_remover, name="log-remover"),
    path("drag_and_drop/", views.log_drag_and_drop, name="log-drag-and-drop"),
]
