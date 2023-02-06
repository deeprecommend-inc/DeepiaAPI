from django.urls import path, include
from rest_framework import routers
import log.urls as log_urls
import user.urls as user_urls
import category.urls as category_urls
import category_log.urls as category_log_urls
from deepia_api import views

urlpatterns = [
    path('api/category/', include(category_urls)),
    path('api/category/log/', include(category_log_urls)),
    path('api/log/', include(log_urls)),
    path('api/user/', include(user_urls)),
    path('api/current_user/', views.current_user, name="current-user"),
    path('api/auth/', views.login, name="login"),
]
