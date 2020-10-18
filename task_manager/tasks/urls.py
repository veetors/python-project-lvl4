from django.urls import path
from task_manager.tasks import views

app_name = 'tasks'
urlpatterns = [
    path('', views.TasksList.as_view(), name='task_list'),
    path('new/', views.TaskCreate.as_view(), name='task_new'),
    path('<int:pk>/', views.TaskDetail.as_view(), name='task_detail'),
    path(
        '<int:pk>/update/',
        views.TaskUpdate.as_view(),
        name='task_update',
    ),
    path(
        '<int:pk>/delete/',
        views.TaskDelete.as_view(),
        name='task_delete',
    ),
]
