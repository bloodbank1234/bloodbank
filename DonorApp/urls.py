from django.urls import path,include
from DonorApp import views

urlpatterns = [
    path('login', views.login),
    path('Register', views.Register),
    path('RegAction', views.RegAction),
    path('LogAction', views.LogAction),
    path('VerifyAction', views.VerifyAction),
    path('home', views.home),
    path('profile', views.profile),
    path('UpdateProfile', views.UpdateProfile),
    path('DeleteProfile', views.DeleteProfile),
    path('UpdateAction', views.UpdateAction),
    path('Request', views.Request),
    path('RequestAction', views.RequestAction),
    path('ViewDonations', views.ViewDonations),
    path('chatbot', views.chatbot),
    path('ChatAction', views.ChatAction),
    path('ViewAlert', views.ViewAlert),
    path('AcceptRequest', views.AcceptRequest),
    path('Predict', views.Predict),
    path('PredictAction', views.PredictAction),
]