from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   path("", views.index, name="index"),
   path('register/', views.register, name='register'),
   path('login/', views.loginPage, name='login'),
   path('logout/', views.logoutUser, name='logout'),
   path('personal/', views.personal, name='personal'),
   path('recent_activity/', views.recent_activity, name='recent_activity'),
   path('like_post/<slug:slug>/', views.like_post, name='like_post'),
   path('contact/', views.contact, name='contact'),
   path('search/', views.search_posts, name='search_posts'),
   path("<str:slug>", views.post_detail, name='post_detail'),
   # path("category/<str:slug>", views.category, name="category"),
   path('<slug:slug>/add_comment/', views.add_comment, name='add_comment'),
   path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
   path('category/<slug:category_slug>/', views.category_posts, name='category'),
   path('<slug:slug>/save/', views.save_post, name='save_post'),
   path('password_reset/', views.password_reset_request, name='password_reset_request'),
   path('password_reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)