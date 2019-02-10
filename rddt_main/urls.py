from django.urls import path
from . import views

app_name = 'rddt_main'

urlpatterns = [
    path('', views.PostListView.as_view(), name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('post/create/', views.create_post, name='newpost'),
    path('post/<int:post_id>/', views.post_page, name='post'),
    path('post/<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('post/<int:post_id>/reply/', views.comment_reply, name='comment_reply'),
]
