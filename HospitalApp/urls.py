from django.urls import path,include
from HospitalApp import views

urlpatterns = [
    path('login', views.login),
    path('Register', views.Register),
    path('RegAction', views.RegAction),
    path('LogAction', views.LogAction),
    path('DonorRequest', views.DonorRequest),
    path('home', views.home),
    path('AcceptDonation', views.AcceptDonation),
    path('RejectDonation', views.RejectDonation),
    path('Request', views.Request),
    path('AcceptRequest', views.AcceptRequest),
    path('RejectRequest', views.RejectRequest),
    path('UrgentRequest', views.UrgentRequest),
    path('RequestAlertAction', views.RequestAlertAction),
    path('AlertStatus', views.AlertStatus),

]