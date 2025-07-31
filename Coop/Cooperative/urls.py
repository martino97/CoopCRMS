from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('add-visitor/', views.add_visitor, name='add_visitor'),
    path('send-mass-sms/', views.send_mass_sms, name='send_mass_sms'),
    path('mobile-signature/<str:session_id>/', views.mobile_signature, name='mobile_signature'),
]
