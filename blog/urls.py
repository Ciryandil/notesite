from django.urls import path

from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<username>/myfeed', views.create_feed, name='feed_list'),
    path('post/new/', views.post_new, name = 'post_new'),
    path('post/search',views.SearchView.as_view(), name='search_all'),
    path('post/vote/<slug:slug>/<int:value>', views.vote, name = 'vote'),
    path('post/<slug:slug>/', views.post_detail, name = 'post_detail'),
    
    path('post/<slug:slug>', views.post_edit, name='post_edit'),
    path('profile/<username>', views.profile, name='profile'),
    path('profile/<username>/search', views.SearchUserView.as_view(), name='search_user'),
    path('profile/<username>/follow', views.set_follow, name = 'follow_user'),
    path('profile/<username>/unfollow', views.set_unfollow, name = 'unfollow_user'),
    path('profile/<username>/setdp', views.set_picture, name = 'setdp'),
    path('profile/<username>/userlist/<slug:slug>', views.get_userlist, name = 'get_users'),
    path('profile/<username>/<slug:slug>',views.get_tagged_user, name='get_tagged_user'),
    path('register/', views.register, name = 'register'),
    path('post/<slug:slug>/post-comment', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<slug:slug>/remove/', views.post_remove, name='post_remove'),
    path('post/<slug:slug>/note/', views.get_note, name='get_note'),
    path('post/tag/<slug:slug>/follow_topic', views.add_topic, name='follow_topic'),
    path('post/tag/<slug:slug>/unfollow_topic', views.remove_topic, name='unfollow_topic'),
    path('post/tag/<slug:slug>', views.get_tagged, name='get_tagged'),
    


]