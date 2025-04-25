from django.contrib import admin
from django.urls import include, path
from .import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.user, name='user'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('categorys/', views.category, name='category'),
    path('categorys/update/<int:category_id>/', views.update_category, name='update_category'),
    path('categorys/add/', views.add_category, name='add_category'),
    path('categorys/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('posts/', views.post, name='post'),
    path('posts/add/', views.add_post, name='add_post'),
    path('posts/update/<int:post_id>/', views.update_post, name='update_post'), 
    path('posts/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('posts/version/<int:version_id>/', views.view_post_version, name='view_post_version'),
    path('comments/', views.comment, name='comment'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
