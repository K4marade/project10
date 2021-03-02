from django.urls import path
from django.contrib.auth import views as auth_views

from account import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True),
        name="login"),
    path('register/', views.register_view, name="register"),
    path('lougout/', views.logout_view, name="logout"),
    path('profile/', views.profile_view, name="profile"),
    path('favorite/', views.favorite_view, name="favorite"),
]
