from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from vault import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vault.urls')),  # Vault app urls
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='vault/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup_view, name='signup'),  # ✅ signup route
    path('accounts/', include('allauth.urls')),
]

