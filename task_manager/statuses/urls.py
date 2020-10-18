from django.urls import path
from task_manager.statuses import views

app_name = 'statuses'
urlpatterns = [
    path('', views.StatusList.as_view(), name='status_list'),
    path('new/', views.StatusCreate.as_view(), name='status_new'),
    path(
        '<int:pk>/update/',
        views.StatusUpdate.as_view(),
        name='status_update',
    ),
    path(
        '<int:pk>/delete/',
        views.StatusDelete.as_view(),
        name='status_delete',
    ),
]
