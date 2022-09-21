from django.urls import path
from .views import login,home,create_comapny,getCompany,delete_team,logout,delete_company,contact
from .views import LoginAPIView,CreateCompany,CreateTeam,getCompanyAPI,getAllTeams,searchCompany_byName
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
    path('create_company1/',CreateCompany.as_view(),name='createCompany1'),
    path('create_team1/<str:id>/',CreateTeam.as_view(),name='createTeam1'),
    path('get_company1/<str:id>/',getCompanyAPI.as_view(),name='getCompany1'),
    path('get_teams1/<str:id>/',getAllTeams.as_view(),name="getAllTeams"),
    path('search_name/',searchCompany_byName.as_view(),name="searchByName"),

]