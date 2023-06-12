from django.urls import path
from user import views

urlpatterns = [
    path("", views.user_list, name="user-list"),
    path("<int:pk>/", views.user_detail, name="user-detail"),
    path("is_unique_email/", views.is_unique_email, name="user-unique-email"),
    path("purple/<int:pk>/", views.user_purple_update, name="user-purple-update"),
    path("admin/", views.user_list_for_admin, name="user-list-for-admin")
]
