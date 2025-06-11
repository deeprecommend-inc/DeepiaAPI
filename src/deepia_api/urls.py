from django.urls import path, include
from rest_framework import routers
import content.urls as content_urls
import user.urls as user_urls
import like.urls as like_urls
from deepia_api import views

urlpatterns = [
    path('api/content/', include(content_urls)),
    path('api/user/', include(user_urls)),
    path('api/like/', include(like_urls)),
    path('api/current_user/', views.current_user, name="current-user"),
    path('api/auth/login/', views.login, name="login"),
    path('api/auth/register/', views.register, name="register"),
    path('api/auth/verify/<str:token>/', views.verify_email, name="verify-email"),
]
