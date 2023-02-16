from django.urls import path
from content import views

urlpatterns = [
    path("", views.content_list, name="content-list"),
    path("user/", views.user_content_list, name="user-content-list"),
    path("<int:pk>/", views.content_detail, name="content-detail"),
]
