from django.urls import path
from task_manager.tags import views

app_name = 'tags'
urlpatterns = [
    path('', views.TagList.as_view(), name='tag_list'),
    path('new/', views.TagCreate.as_view(), name='tag_new'),
    path('<int:pk>/update/', views.TagUpdate.as_view(), name='tag_update'),
    path('<int:pk>/delete/', views.TagDelete.as_view(), name='tag_delete'),
]
