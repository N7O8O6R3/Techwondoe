from django.shortcuts import render,redirect
from .models import Company,Team
from django.contrib.auth import authenticate,login
import jwt, datetime
from CompanyTask.settings import key
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core import serializers
from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions
from .serializers import LoginSerializer,CreateCompanySerializer,CreateTeamSerializer
import uuid
import json
from django.http.response import JsonResponse

def login(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(email=username).first()
        if user is None:
            return render(request,'login.html',{'msg':'User not Found'})
        if not user.check_password(password):
            return render(request,'login.html',{'msg':'Incorrect Password'})
        if not user.is_superuser:
            return render(request,'login.html',{'msg':'Access Given only to Super Admin'}) 
        exp = datetime.datetime.utcnow() + (datetime.timedelta(minutes=60) )
        payload = {
            # 'id':user.id,
            'username':username,
            'exp':exp,
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, key, algorithm ='HS256') #.decode('utf-8')
        print("login jwt token created \ntoken -->",token)
        response = redirect("home")
        # login(request,user)
        response.set_cookie(key='token', value=token, httponly=True)
        print("Token set to cookies with key 'token'")
        return response
    return render(request,'login.html')

def home(request):
    token = request.COOKIES.get('token', None)
    if token==None:
        return redirect("login")
    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
        print(payload)
        company_details=Company.objects.all()
        return render(request,'home.html',{'company_details':company_details})
    except jwt.ExpiredSignatureError:
        return redirect("login")



def create_comapny(request):
    token = request.COOKIES.get('token', None)
    if token==None:
        return redirect("login")

    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
        if request.method=='POST':
            print(request.POST)
            company=Company.objects.create(companyName=request.POST['companyName'],companyCEO=request.POST['companyCEO'],companyAddress=request.POST['companyAddress'],inceptionDate=request.POST['inceptionDate'])
            if company is not None:
                company.save()
                return render(request,'create_company.html',{'msg':'Company Creation Successful','color':'green'})
            else:
                return render(request,'create_company.html',{'msg':'Company Creation Failed','color':'red'})
        return render(request,'create_company.html')
    except jwt.ExpiredSignatureError:
        return redirect("login")
    

def getCompany(request):
    token = request.COOKIES.get('token', None)
    if token==None:
        return redirect("login")

    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
        if 'id' in request.GET:
            company= Company.objects.get(id=request.GET['id']) 
            context={}
            if request.method=='POST':
                team=Team.objects.create(teamLeadName=request.POST['teamLeadName'],companyID=company)
                if team is not None:
                    team.save()
                    context['msg']='Team Creation Successful'
                    context['color']='green'
                else:
                    context['msg']='Team Creation Failed'
                    context['color']='red'
                print(request.POST)
            
            context['company']=company
            teams=Team.objects.filter(companyID=request.GET['id'])
            context['teams']=teams
            for i in teams:
                print(i.companyID,i.teamLeadName,i.id,i.companyID.companyName)
            return render(request,'company.html',context=context)
        else:
            return redirect('home')
    except jwt.ExpiredSignatureError:
        return redirect("login")
    

def delete_team(request):
    token = request.COOKIES.get('token', None)
    if token==None:
        return redirect("login")
    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
        if 'id' in request.GET:
            team=Team.objects.get(id=request.GET['id'])
            companyid= team.companyID.id
            if team is not None:
                team.delete()
            return redirect('/company/?id='+str(companyid))
        else:
            return redirect(home)
    except jwt.ExpiredSignatureError:
        return redirect("login")

def delete_company(request):
    token = request.COOKIES.get('token', None)
    if token==None:
        return redirect("login")
    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
        if 'id' in request.GET:
            company=Company.objects.get(id=request.GET['id'])
            company.delete()
            return redirect('home')
        else:
            return redirect('home')
    except jwt.ExpiredSignatureError:
        return redirect("login")

    

def logout(request):
    response = redirect('login')
    response.delete_cookie('token')
    return response

def contact(request):
    token = request.COOKIES.get('token', None)
    if token==None:
        return redirect("login")
    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
        return render(request,'contact.html')
    except jwt.ExpiredSignatureError:
        return redirect("login")



def search_byName(request):
    company=Company.objects.filter(companyName=request.POST['name'])
        



#POSTMAN APIS
class LoginAPIView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer
    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        try:
            serializer.is_valid(raise_exception=True)
            print(serializer.data)
            return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data':data}, status=status.HTTP_200_OK)


class CreateCompany(generics.GenericAPIView):
    serializer_class = CreateCompanySerializer
    permission_classes = ([IsAuthenticated])
    # renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        print(user,request.user.email)
        superuser = User.objects.get(email=request.user.email)
        if superuser.is_superuser:
            #company={'companyName':request.data['companyName'],'companyCEO':request.data['companyCEO'],'companyAddress':request.data['companyAddress'],'inceptionDate':request.data['inceptionDate']}
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            company_data = serializer.data
            return Response(company_data, status=status.HTTP_201_CREATED)
        return Response({'detail':"You don't have permission to perofrm this operation"}, status=status.HTTP_400_BAD_REQUEST)
        
class CreateTeam(generics.GenericAPIView):
    # serializer_class = CreateTeamSerializer
    permission_classes = ([IsAuthenticated])

    def post(self,request,id):
        print(request.data,id)
        if 'teamLeadName' in request.data:
            superuser=User.objects.get(email=request.user.email)
            if superuser.is_superuser:
                company=Company.objects.get(id=id)
                print(company,company.companyName)
                team=Team.objects.create(teamLeadName=request.data['teamLeadName'],companyID=company)
                # team={'teamLeadName':request.data['teamLeadName'],'companyID':company}
                print(team)
                if team is not None:
                    team.save()
                obj=serializers.serialize('python', [team,])
                #return JsonResponse(obj, safe=False)
                return Response(obj, status=status.HTTP_201_CREATED)
            return Response({'detail':"You don't have permission to perofrm this operation"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail':"Team Lead Name is required"},status=status.HTTP_400_BAD_REQUEST)

class getCompanyAPI(generics.GenericAPIView):
    permission_classes = ([IsAuthenticated])

    def get(self,request,id):
        superuser=User.objects.get(email=request.user.email)
        if superuser.is_superuser:
            company=Company.objects.get(id=id)
            obj=serializers.serialize('python', [company,])
            #return JsonResponse(obj, safe=False)
            return Response(obj, status=status.HTTP_201_CREATED)
        return Response({'detail':"You don't have permission to perofrm this operation"}, status=status.HTTP_400_BAD_REQUEST)

class getAllTeams(generics.GenericAPIView):
    permission_classes=([IsAuthenticated])

    def get(self,request,id):
        superuser=User.objects.get(email=request.user.email)
        
        if superuser.is_superuser:
            company=Company.objects.get(id=id)
            teams=Team.objects.filter(companyID=company.id)
            # print(teams)
            obj=serializers.serialize('python', teams)
            #return JsonResponse(obj, safe=False)
            return Response(obj, status=status.HTTP_200_OK)
        return Response({'detail':"You don't have permission to perofrm this operation"}, status=status.HTTP_400_BAD_REQUEST)


class searchCompany_byName(generics.GenericAPIView):
    permission_classes=([IsAuthenticated])

    def post(self,request):
        superuser=User.objects.get(email=request.user.email)
        if 'companyName' in request.data:
            if superuser.is_superuser:
                company=Company.objects.filter(companyName=request.data['companyName'])
                obj=serializers.serialize('python', company)
                #return JsonResponse(obj, safe=False)
                return Response(obj, status=status.HTTP_200_OK)
            return Response({'detail':"You don't have permission to perofrm this operation"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail':"Search Query companyName is required"},status=status.HTTP_400_BAD_REQUEST)