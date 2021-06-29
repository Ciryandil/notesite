from django.urls import path

from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name = 'post_new'),
    path('post/search',views.SearchView.as_view(), name='search_all'),
    path('post/<slug:slug>/', views.post_detail, name = 'post_detail'),
    path('post/<slug:slug>', views.post_edit, name='post_edit'),
    path('profile/<username>', views.profile, name='profile'),
    path('profile/<username>/search', views.SearchUserView.as_view(), name='search_user'),
    path('profile/<username>/set_dp', views.set_picture, name = 'set_dp'),
    path('profile/<username>/<slug:slug>',views.get_tagged_user, name='get_tagged_user'),
    path('register/', views.register, name = 'register'),
    path('post/<slug:slug>/post-comment', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<slug:slug>/remove/', views.post_remove, name='post_remove'),
    path('post/<slug:slug>/note/', views.get_note, name='get_note'),
    path('post/tag/<slug:slug>', views.get_tagged, name='get_tagged'),


]