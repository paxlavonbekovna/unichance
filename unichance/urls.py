from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='unichance_dashboard'),
    path('profile/', views.profile_settings_view, name='profile_settings'),
    path('universities/', views.universities_directory_view, name='universities_directory'),
    
    path('api/search/', views.university_search_api, name='university_search_api'),
    path('api/all-universities/', views.all_universities_api, name='all_universities_api'),
    path('api/toggle-document/<int:doc_id>/', views.toggle_document_status_api, name='toggle_document_status_api'),
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('university/<str:university_name>/', views.university_profile_view, name='university_profile'),
    path('dashboard/documents/', views.document_examples_view, name='document_examples'),
]