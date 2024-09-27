from rest_framework.response import Response
from .seializers import Sep_dashboard_Serilizaer
from inside.models import Sep_dashboard
from django.db.models import Q
# from django.http import JsonResponse
from rest_framework.decorators import api_view
from .seializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import generics
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
import pandas as pd

@api_view(['GET','POST'])
def database_view(request):
    if request.method=='GET':
        data=Sep_dashboard.objects.all()
        res=Sep_dashboard_Serilizaer(data,many=True)
        offset = request.GET.get("offset", None)
        limit = request.GET.get('limit', None)
        if offset is not None and limit is not None:
            offset = int(offset)
            limit = int(limit)
            return Response(res.data[offset:offset+limit])
        return Response(res.data)
    if request.method=='POST':
        serilizer=Sep_dashboard_Serilizaer(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data)
        else:
            return Response(serilizer.errors)

# class dashboard(generics.ListAPIView):
#     queryset = Sep_dashboard.objects.all()
#     serializer_class = Sep_dashboard_Serilizaer
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         offset=self.request.query_params.get("offset",None)
#         limit=self.request.query_params.get('limit',None)
#         # data = Sep_dashboard.objects.all()
#         # res = Sep_dashboard_Serilizaer(data, many=True)
#         if offset is not None and limit is not None:
#             offset=int(offset)
#             limit=int(offset)
#             return queryset[offset:offset+limit]
#         return queryset
    # def post(self):
    #     serilizer = Sep_dashboard_Serilizaer(data=request.data)
    #     if serilizer.is_valid():
    #         serilizer.save()
    #         return Response(serilizer.data)
    #     else:
    #         return Response(serilizer.errors)
# class dashboard_search(generics.ListAPIView):
#     queryset = Sep_dashboard.objects.all()
#     serializer_class = Sep_dashboard_Serilizaer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields =['STANDARD_SETTING','STANDARD','Technology','PATENT_OWNER','Inventor']

def evaluate_data(res):
    count = {'Inventor': '', 'PATENT_OWNER': '', 'Patent_Number': '', 'SSO': '', 'STANDARD': '', 'Sub_Technology': '',
             'Technology': ''}
    try:
        df = pd.DataFrame(res.data)
        count['SSO'] = len(df.drop_duplicates(['STANDARD_SETTING']).values)
        count['STANDARD'] = len(df.drop_duplicates(['STANDARD']).values)
        count['Technology'] = len(df.drop_duplicates(['Technology']).values)
        count['PATENT_OWNER'] = len(df.drop_duplicates(['PATENT_OWNER']).values)
        count['Sub_Technology'] = len(df.drop_duplicates(['Sub_Technology']).values)
        count['Patent_Number'] = len(df.drop_duplicates(['Patent_Number']).values)
        count['Inventor'] = len(df.drop_duplicates(['Inventor']).values)
        result = {'total': len(df), 'cat_count': count}
        return result
    except:
        result = {'total': 0, 'cat_count': count}
        return result


@api_view(['GET'])
def database_count(request):
    tech=request.GET.getlist("TECH[]",[])
    stand_sett=request.GET.getlist("STANDARD_SET[]",[])
    patent=request.GET.get("PATENT_OWNER",'')
    stand=request.GET.get("STANDARD",'')
    IPRD_REF=request.GET.get('IPRD_REFERENCE','')
    Patent_num =request.GET.get('PATENT_NUM', '')
    Sub_Technology=request.GET.get('Sub_Tech', '')
    from_date=request.GET.get('DATE_FROM','')
    to_date = request.GET.get('DATE_TO','')
    offset = request.GET.get("offset", None)
    limit =  request.GET.get('limit', None)

    if from_date!="" and to_date!="":
        data = Sep_dashboard.objects.filter(Q(Technology__in=tech)
                                            & Q(STANDARD__icontains=stand)
                                            & Q(STANDARD_SETTING__in=stand_sett)
                                            & Q(PATENT_OWNER__icontains=patent) & Q(IPRD_REFERENCE__icontains=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__icontains=Sub_Technology)
                                            & Q(IPRD_SIGNATURE_DATE__gte=from_date)
                                            & Q(IPRD_SIGNATURE_DATE__lte=to_date))
    elif len(stand_sett)>0 and len(tech)>0:
        # data = Sep_dashboard.objects.filter(Technology__in=eval(tech))
        data = Sep_dashboard.objects.filter(Q(Technology__in=tech)
                                            & Q(STANDARD_SETTING__in=stand_sett)
                                            & Q(STANDARD__icontains=stand)
                                            & Q(PATENT_OWNER__icontains=patent) & Q(IPRD_REFERENCE__icontains=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__icontains=Sub_Technology))
    elif len(stand_sett)>0:
        data = Sep_dashboard.objects.filter(Q(STANDARD_SETTING__in=stand_sett)
                                            & Q(STANDARD__icontains=stand)
                                            & Q(PATENT_OWNER__icontains=patent) & Q(IPRD_REFERENCE__icontains=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__icontains=Sub_Technology))
    elif len(tech)>0:
        data = Sep_dashboard.objects.filter(Q(Technology__in=tech)
                                            & Q(STANDARD__icontains=stand)
                                            & Q(PATENT_OWNER__icontains=patent) & Q(IPRD_REFERENCE__icontains=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__icontains=Sub_Technology))
    else:
        data = Sep_dashboard.objects.filter(Q(STANDARD__icontains=stand)
                                            & Q(PATENT_OWNER__icontains=patent) & Q(IPRD_REFERENCE__icontains=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__icontains=Sub_Technology))


    res = Sep_dashboard_Serilizaer(data, many=True)
    count_data= evaluate_data(res)
    if offset is not None and limit is not None:
        offset = int(offset)
        limit = int(limit)
        return Response({'result':res.data[offset:offset+limit],'count':count_data})
    else:
        return Response({'result': res.data, 'count': count_data})

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

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passesd for {}".format(request.user.email))