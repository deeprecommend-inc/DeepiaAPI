from django.urls import path
from . import views

urlpatterns = [
    path('content/<int:content_id>/', views.content_comments, name='content-comments'),
    path('<int:comment_id>/', views.comment_detail, name='comment-detail'),
    path('like/', views.toggle_like, name='toggle-like'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle-follow'),
    path('followers/<int:user_id>/', views.user_followers, name='user-followers'),
    path('following/<int:user_id>/', views.user_following, name='user-following'),
]