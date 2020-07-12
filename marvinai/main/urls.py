from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('CreateReseller/', views.CreateReseller, name='CreateReseller'),
    path('ViewReseller/<str:pk>', views.ViewReseller, name='ViewReseller'),
    path('EditReseller/<str:pk>', views.EditReseller, name='EditReseller'),
    path('DeleteReseller/<str:pk>', views.DeleteReseller, name='DeleteReseller'),

    path('ViewReseller/<str:pk>/dashboard', views.ResellerDashboard, name='ResellerDashboard'),
    path('ViewReseller/<str:pk>/settings', views.ResellerSettings, name='ResellerSettings'),

    path('CreateCustomer/', views.CreateCustomer, name='CreateCustomer'),
    path('ViewCustomer/<str:pk>', views.ViewCustomer, name='ViewCustomer'),
    path('EditCustomer/<str:pk>', views.EditCustomer, name='EditCustomer'),
    path('DeleteCustomer/<str:pk>', views.DeleteCustomer, name='DeleteCustomer'),

    path('ViewCustomer/<str:pk>/dashboard', views.CustomerDashboard, name='CustomerDashboard'),
    path('ViewCustomer/<str:pk>/settings', views.CustomerSettings, name='CustomerSettings'),
    path('ViewCustomer/<str:pk>/training', views.CustomerNLUTraining, name='CustomerNLUTraining'),
    path('post/ajax/nlutrainingupdate', views.NLUTrainingUpdate, name='nlutrainingupdate'),
    path('ViewCustomer/<str:pk>/response', views.CustomerResponse, name='CustomerResponse'),
    path('post/ajax/responseupdate', views.ResponseUpdate, name='responseupdate'),
    path('ViewCustomer/<str:pk>/stories', views.CustomerStories, name='CustomerStories'),
    path('post/ajax/storiesupdate', views.StoriesUpdate, name='storiesupdate'),
    path('ViewCustomer/<str:pk>/domain', views.CustomerDomain, name='CustomerDomain'),
    path('ViewCustomer/<str:pk>/configuration', views.CustomerConfiguration, name='CustomerConfiguration'),
    path('ViewCustomer/<str:pk>/logs', views.CustomerLogs, name='CustomerLogs'),
    path('ViewCustomer/<str:pk>/trainbot', views.CustomerTrainBot, name='CustomerTrainBot'),
    path('post/ajax/trainbot', views.TrainBotBackend, name='trainbot'),
    path('ViewCustomer/<str:pk>/license', views.CustomerLicense, name='CustomerLicense'),
    path('ViewCustomer/<str:pk>/messages', views.CustomerMessages, name='CustomerMessages'),
    path('post/ajax/chathistoryupdate', views.ChatHistoryUpdate, name='chathistoryupdate'),
]
