from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('add/', views.add_todo, name='add_todo'),
    path('toggle/<int:pk>/', views.toggle_todo, name='toggle_todo'),
    path('edit/<int:pk>/', views.edit_todo, name='edit_todo'),
    path('delete/<int:pk>/', views.delete_todo, name='delete_todo'),
    path('clear-completed/', views.clear_completed, name='clear_completed'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]