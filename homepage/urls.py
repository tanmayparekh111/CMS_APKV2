from django.urls import path
from . import views

urlpatterns = [

    path('signup/', views.signup, name='signup'),
    
    path('login_user/', views.login_user, name='login_user'),

    path('feeds/', views.feeds, name='feeds'),

    path('make_post/', views.make_post, name='make_post'),
    path('delete_post/', views.delete_post, name='delete_post'),
    

    path('like_feeds/', views.like_feeds, name='like_feeds'),
    path('dislike_feeds/', views.dislike_feeds, name='dislike_feeds'),

    path('delete_user/', views.delete_user, name='delete_acc'),
    path('logout_user/', views.logout_user, name='logout_user'),

    # extra for testing purpose.
    path('get_all_users/', views.get_all_users, name='get_all_users'),
]
