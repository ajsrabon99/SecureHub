from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/add/', views.contact_add, name='contact_add'),
    path('contacts/edit/<int:pk>/', views.contact_edit, name='contact_edit'),
    path('contacts/delete/<int:pk>/', views.contact_delete, name='contact_delete'),
    
    path('links/', views.link_list, name='link_list'),
    path('links/add/', views.link_add, name='link_add'),
    path('links/edit/<int:pk>/', views.link_edit, name='link_edit'),
    path('links/delete/<int:pk>/', views.link_delete, name='link_delete'),

    path('passwords/', views.password_list, name='password_list'),
    path('passwords/add/', views.password_add, name='password_add'),
    path('passwords/edit/<int:pk>/', views.password_edit, name='password_edit'),
    path('passwords/delete/<int:pk>/', views.password_delete, name='password_delete'),
]
