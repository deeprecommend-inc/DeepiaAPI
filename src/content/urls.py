from django.urls import path
from content import views

urlpatterns = [
    path("", views.content_list, name="content-list"),
    path("create/", views.content_create, name="content-create"),
    path("user/", views.user_content_list, name="user-content-list"),
    path("<int:pk>/", views.content_detail, name="content-detail"),
    path("piapi/generate/", views.piapi_generate, name="piapi-generate"),
    path("piapi/status/<str:generation_id>/", views.piapi_status, name="piapi-status"),
    path("workflow/save/", views.workflow_save, name="workflow-save"),
    path("workflow/list/", views.workflow_list, name="workflow-list"),
    path("workflow/<int:pk>/", views.workflow_detail, name="workflow-detail"),
]
