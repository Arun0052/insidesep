from django.http import JsonResponse
from rest_framework.response import Response
from .seializers import Sep_dashboard_Serilizaer,PasswordResetRequestSerializer,SetNewPasswordSerializer
from inside.models import Sep_dashboard
from django.db.models import Q, F
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
from dal import autocomplete
# views.py
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# from .serializers import
# # views.py
# from .serializers import

class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                serializer = SetNewPasswordSerializer(data=request.data)
                if serializer.is_valid():
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()
                    return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                # reset_url = request.build_absolute_uri(
                #     reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                # )
                reset_url=f"http://insidesep.com:3000/reset-password?token={token}&uidb64={uid}"
                send_mail(
                    'Password Reset Request',
                    f'Use the following link to reset your password: {reset_url}',
                    'vs8029714@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
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
        if isinstance(request.data, list):
            # If it's a list, validate and save each item
            serializer = Sep_dashboard_Serilizaer(data=request.data, many=True)
        else:
            # Otherwise, handle as a single item
            serializer = Sep_dashboard_Serilizaer(data=request.data)
            # Validate and save if data is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # serilizer=Sep_dashboard_Serilizaer(data=request.data)
        # if serilizer.is_valid():
        #     serilizer.save()
        #     return Response(serilizer.data)
        # else:
        #     return Response(serilizer.errors)

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
#     def post(self):
#         serilizer = Sep_dashboard_Serilizaer(data=request.data)
#         if serilizer.is_valid():
#             serilizer.save()
#             return Response(serilizer.data)
#         else:
#             return Response(serilizer.errors)
# class dashboard_search(generics.ListAPIView):
#     queryset = Sep_dashboard.objects.all()
#     serializer_class = Sep_dashboard_Serilizaer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields =['STANDARD_SETTING','STANDARD','Technology','PATENT_OWNER','Inventor']



class PatentsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated:
        #     return Sep_dashboard.objects.none()
        qs = Sep_dashboard.objects.values_list('Patent_Number', flat=True).distinct()
        if self.q:
            qs = qs.filter(Patent_Number__icontains=self.q)
        return qs

    def get(self, request, *args, **kwargs):
        # Override the get method to return JSON response with a list of patent numbers
        qs = self.get_queryset()
        return JsonResponse({'results': [{'id': p, 'text': p} for p in qs]})

# def evaluate_data(res):
#     count = {'Inventor': '', 'PATENT_OWNER': '', 'Publication_Number': '', 'SSO': '', 'STANDARD': '', 'Sub_Technology': '',
#              'Technology': ''}
#     try:
#         df = pd.DataFrame(res.data)
#         count['SSO'] = len(df.drop_duplicates(['STANDARD_SETTING']).values)
#         count['STANDARD'] = len(df.drop_duplicates(['STANDARD']).values)
#         count['Technology'] = len(df.drop_duplicates(['Technology']).values)
#         count['PATENT_OWNER'] = len(df.drop_duplicates(['PATENT_OWNER']).values)
#         count['Sub_Technology'] = len(df.drop_duplicates(['Sub_Technology']).values)
#         count['Publication_Number'] = len(df.drop_duplicates(['Publication_Number']).values)
#         count['Inventor'] = len(df.drop_duplicates(['Inventor']).values)
#         result = {'total': len(df), 'cat_count': count}
#         return result
#     except:
#         result = {'total': 0, 'cat_count': count}
#         return result

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def unique_data(request):
    data = Sep_dashboard.objects.all()
    count = {
        'PATENT_OWNER': list(data.values_list('PATENT_OWNER', flat=True).distinct()),
        'Sub_Technology': list(data.values_list('Sub_Technology', flat=True).distinct()),
        'Publication_Number': list(data.values_list('STANDARD', flat=True).distinct()),
        'IPRD_REFERENCE': list(data.values_list('IPRD_REFERENCE', flat=True).distinct())
    }
    return Response({"result": count})



@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def database_count(request):
    tech=request.GET.getlist("TECH[]",[])
    stand_sett=request.GET.getlist("STANDARD_SET[]",[])
    patent=request.GET.getlist("PATENT_OWNER",[])
    stand=request.GET.getlist("STANDARD",[])
    IPRD_REF=request.GET.getlist('IPRD_REFERENCE',[])
    Patent_num =request.GET.get('PATENT_NUM', '')
    Sub_Technology=request.GET.getlist('Sub_Tech', [])
    from_date=request.GET.get('DATE_FROM','')
    to_date = request.GET.get('DATE_TO','')
    offset = request.GET.get("offset", None)
    limit =  request.GET.get('limit', None)
    if len(tech)>0:
        query = Q()
        for tec in tech:
            query |= Q(Technology__icontains=tec)

    if len(tech)==0 and len(stand_sett)==0 and patent=="" and stand=="" and IPRD_REF=="" and Patent_num=="" and Sub_Technology=="" and from_date=="" and to_date =="":
        data = Sep_dashboard.objects.filter(STANDARD__iexact="ahhh")

    elif from_date!="" and to_date!="" and len(stand_sett)>0 and len(tech)>0:
        data = Sep_dashboard.objects.filter(query
                                            & Q(STANDARD__in=stand)
                                            & Q(STANDARD_SETTING__in=stand_sett)
                                            & Q(PATENT_OWNER__in=patent)
                                            & Q(IPRD_REFERENCE__in=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__in=Sub_Technology)
                                            & Q(IPRD_SIGNATURE_DATE__gte=from_date)
                                            & Q(IPRD_SIGNATURE_DATE__lte=to_date))
    elif from_date!="" and to_date!="" and len(stand_sett)>0:
        data = Sep_dashboard.objects.filter(Q(STANDARD_SETTING__in=stand_sett)
                                            & Q(STANDARD__in=stand)
                                            & Q(PATENT_OWNER__in=patent)
                                            & Q(IPRD_REFERENCE__in=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__in=Sub_Technology)
                                            & Q(IPRD_SIGNATURE_DATE__gte=from_date)
                                            & Q(IPRD_SIGNATURE_DATE__lte=to_date))
    elif from_date!="" and to_date!="" and len(tech)>0:
        data = Sep_dashboard.objects.filter(query
                                            & Q(STANDARD__in=stand)
                                            & Q(PATENT_OWNER__in=patent)
                                            & Q(IPRD_REFERENCE__in=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__in=Sub_Technology)
                                            & Q(IPRD_SIGNATURE_DATE__gte=from_date)
                                            & Q(IPRD_SIGNATURE_DATE__lte=to_date))
    elif len(stand_sett)>0 and len(tech)>0:
        data = Sep_dashboard.objects.filter(query
                                            & Q(STANDARD_SETTING__in=stand_sett)
                                            & Q(STANDARD__in=stand)
                                            & Q(PATENT_OWNER__in=patent)
                                            & Q(IPRD_REFERENCE__i=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__in=Sub_Technology))
    elif len(stand_sett)>0:
        data = Sep_dashboard.objects.filter(Q(STANDARD_SETTING__in=stand_sett)
                                            & Q(STANDARD__in=stand)
                                            & Q(PATENT_OWNER__in=patent)
                                            & Q(IPRD_REFERENCE__in=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__in=Sub_Technology))
    elif len(tech)>0:
        data = Sep_dashboard.objects.filter(query
                                            & Q(STANDARD__in=stand)
                                            & Q(PATENT_OWNER__in=patent)
                                            & Q(IPRD_REFERENCE__in=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__in=Sub_Technology))
    elif from_date!="" and to_date!="":
        data = Sep_dashboard.objects.filter(Q(STANDARD__in=stand)
                                            & Q(PATENT_OWNER__in=patent)
                                            & Q(IPRD_REFERENCE__in=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__in=Sub_Technology)
                                            & Q(IPRD_SIGNATURE_DATE__gte=from_date)
                                            & Q(IPRD_SIGNATURE_DATE__lte=to_date))
    else:
        data = Sep_dashboard.objects.filter(Q(STANDARD__in=stand)
                                            & Q(PATENT_OWNER__in=patent)
                                            & Q(IPRD_REFERENCE__in=IPRD_REF)
                                            & Q(Patent_Number__icontains=Patent_num)
                                            & Q(Sub_Technology__in=Sub_Technology))
    data1 = data.distinct('IPRD_REFERENCE')
    unique_res = Sep_dashboard_Serilizaer(data1, many=True)
    # res = Sep_dashboard_Serilizaer(data, many=True)
    count = {'Inventor': '', 'PATENT_OWNER': '', 'Publication_Number': '', 'SSO': '', 'STANDARD': '',
             'Sub_Technology': '',
             'Technology': ''}
    try:
        count['SSO'] = data.values('STANDARD_SETTING').distinct().count()
        count['STANDARD'] = data.values('STANDARD').distinct().count()
        count['Technology'] = data.values('Technology').distinct().count()
        count['PATENT_OWNER'] = data.values('PATENT_OWNER').distinct().count()
        count['Sub_Technology'] = data.values('Sub_Technology').distinct().count()
        count['Publication_Number'] = data.values('Publication_Number').distinct().count()
        count['Inventor'] = data.values('Inventor').distinct().count()
        count_data = {'total': data.count(), 'cat_count': count}
#     return JsonResponse(result)
    except Exception as e:
        count_data = {'total': 0, 'cat_count': count}
        # return JsonResponse(result)
    # count_data= evaluate_data(res)
    if offset is not None and limit is not None:
        offset = int(offset)
        limit = int(limit)
        return Response({'result':unique_res.data[offset:offset+limit],'count':count_data})
    else:
        return Response({'result': unique_res.data, 'count': count_data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_database(request):
    IPRD_REF=request.GET.get('IPRD_REFERENCE','')
    data = Sep_dashboard.objects.filter(Q(IPRD_REFERENCE__icontains=IPRD_REF)).order_by('DIPG_DISPLAY_NUMBER')
    res = Sep_dashboard_Serilizaer(data, many=True)
    return Response(res.data)


@api_view(['GET','PUT','DELETE'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
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