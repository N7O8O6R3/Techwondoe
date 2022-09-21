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
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions
from .serializers import LoginSerializer

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