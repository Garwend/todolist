from django.urls import path
from . import views

urlpatterns = [
    path('', views.TasksList.as_view(), name='tasks-list-create'),
    path('<int:id>/', views.TaskDetail.as_view(), name='task-get-delete'),
]
