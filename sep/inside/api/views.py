from rest_framework.response import Response
from .seializers import Sep_dashboard_Serilizaer
from inside.models import Sep_dashboard
# from django.http import JsonResponse
from rest_framework.decorators import api_view
from .seializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
@api_view(['GET','POST'])
def database_view(request):
    if request.method=='GET':
        data=Sep_dashboard.objects.all()
        res=Sep_dashboard_Serilizaer(data,many=True)
        return Response(res.data)
    if request.method=='POST':
        serilizer=Sep_dashboard_Serilizaer(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data)
        else:
            return Response(serilizer.errors)

@api_view(['GET','PUT','DELETE'])
def patents_view(request,pk):
    if request.method=='GET':
        patents=Sep_dashboard.objects.get(pk=pk)
        serilizer=Sep_dashboard_Serilizaer(patents)
        return Response(serilizer.data)
    if request.method=='PUT':
        patents = Sep_dashboard.objects.get(pk=pk)
        serilizer = Sep_dashboard_Serilizaer(patents,request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data)
        else:
            return Response(serilizer.errors)
    if request.method=='DELETE':
        sep=Sep_dashboard.objects.get(pk=pk)
        sep.delete()
        return Response("sucess")

@api_view(['POST'])
def signup(request):
    serilizer= UserSerializer(data=request.data)
    if serilizer.is_valid():
        serilizer.save()
        user=User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token=Token.objects.create(user=user)
        return Response({"token":token.key,"user":serilizer.data})
    return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user=get_object_or_404(User,username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"not found"},status=status.HTTP_404_NOT_FOUND)
    token,created=Token.objects.get_or_create(user=user)
    serializer =UserSerializer(instance=user)
    return Response({"token":token.key,"user":serializer.data})