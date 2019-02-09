from django.urls import path
from . import views

app_name = 'rddt_main'

urlpatterns = [
    path('', views.PostListView.as_view(), name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('post/create', views.create_post, name='newpost'),
]
