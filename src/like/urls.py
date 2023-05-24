from django.urls import path
from like import views

urlpatterns = [
    path("", views.like_list, name="like-list"),
    path("<int:pk>/", views.like_detail, name="like-detail"),
]
