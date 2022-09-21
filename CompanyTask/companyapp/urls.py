from django.urls import path
from .views import login,home,create_comapny,getCompany,delete_team,logout,delete_company,contact
from .views import LoginAPIView
urlpatterns = [
    path('',home,name='home'),
    path('login/', login,name='login'),
    path('create_company/',create_comapny,name='createCompany'),
    path('company/',getCompany,name='getCompany'),
    path('delete_team/',delete_team,name='deleteTeam'),
    path('logout/',logout,name='logout'),
    path('delete_company/',delete_company,name='deleteCompany'),
    path('contact/',contact,name='contact'),

    #Postman URLS
    path('login1/', LoginAPIView.as_view(), name="login1"),

]