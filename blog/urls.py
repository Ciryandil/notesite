from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name = 'post_new'),
    path('post/<slug:slug>/', views.post_detail, name = 'post_detail'),
    path('post/<slug:slug>', views.post_edit, name='post_edit'),
    path('profile/<username>', views.profile, name='profile'),
    path('register/', views.register, name = 'register'),
    path('post/<slug:slug>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<slug:slug>/remove/', views.post_remove, name='post_remove'),

]