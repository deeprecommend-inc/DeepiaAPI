from django.urls import path
from category_log import views

urlpatterns = [
    path("<int:pk>/", views.category_log_list, name="category-log-list"),
    path("", views.update_categories, name="update-categories"),
]
