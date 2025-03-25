from django.urls import path,include
from AdminApp import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('LogAction', views.LogAction),
    path('home', views.home),
    path('AddHsp', views.AddHsp),
    path('AddHspAction', views.AddHspAction),
    path('ViewHsp', views.ViewHsp),
    path('Accepthsp', views.Accepthsp),
    path('deletehsp', views.deletehsp),
    path('search', views.search),
    path('SearchAction', views.SearchAction),
    path('RequestForBlood', views.RequestForBlood),
    path('RequestAction', views.RequestAction),
    path('BRequestStatus', views.BRequestStatus),
    path('donorlist', views.donorlist),
    # path('ADDFAQ', views.ADDFAQ),
    path('BotModel', views.BotModel),
    # path('AddFAQAction', views.AddFAQAction),
    path('feedback', views.feedback),
    path('FeedbackAction', views.FeedbackAction),
    path('ViewFeedback', views.ViewFeedback),

]