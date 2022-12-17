from django.urls import path
from category import views

urlpatterns = [
    path("", views.category_list, name="category-list"),
    path("public/", views.public_category_list, name="public-category-list"),
    path("<int:pk>/", views.category_detail, name="category-detail"),
    path("drag_and_drop/", views.category_drag_and_drop, name="category-drag-and-drop"),
]
