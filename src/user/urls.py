from django.urls import path
from user import views

urlpatterns = [
    path("", views.user_list, name="user-list"),
    path("<int:pk>/", views.user_detail, name="user-detail"),
    path("is_unique_email/", views.is_unique_email, name="user-unique-email"),
]
