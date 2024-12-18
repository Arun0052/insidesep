from django.http import JsonResponse
from rest_framework.response import Response
from .seializers import Sep_search_Serilizaer,Sep_dashboard_Serilizaer,PasswordResetRequestSerializer,SetNewPasswordSerializer
from inside.models import Sep_dashboard,Sep_Search,UserProfile
from django.db.models import Q, F
from rest_framework.decorators import api_view
from .seializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from dal import autocomplete
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from myapp.models import UserProfile  # Replace with correct model path

@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def ResetSearchCountAPIView(request):
    if request.method=="POST":
        action = request.data.get('action', None)
        if action != 'reset':
            return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        # Get current time
        # now = timezone.now()
        # Get all user profiles
        user_profiles = UserProfile.objects.all()
        # Loop through the profiles and reset the search count if the user joined more than 24 hours ago
        for user_profile in user_profiles:
            user_profile.search_count = 0
            user_profile.save()
            # if user_profile.user.date_joined < now - timedelta(days=1):

        return Response({"detail": "Search count reset for eligible users."}, status=status.HTTP_200_OK)



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
                try:
                    reset_url = f"https://insidesep.com/reset-password?token={token}&uidb64={uid}"

                    # reset_url=f"http://insidesep.com:3000/reset-password?token={token}&uidb64={uid}"
                    send_mail(
                        'Password Reset Request',
                        f'Use the following link to reset your password: {reset_url}',
                        'insideSEP@patentskart.com',
                        [user.email],
                        fail_silently=False,
                    )
                    return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)
                except:
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
def search_view(request):
    if request.method=='POST':
        if isinstance(request.data, list):
            # If it's a list, validate and save each item
            serializer = Sep_search_Serilizaer(data=request.data, many=True)
        else:
            # Otherwise, handle as a single item
            serializer = Sep_search_Serilizaer(data=request.data)
            # Validate and save if data is valid

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




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
def search_by_attribute(request):
    # Get the attribute name from the request query parameter, defaulting to an empty string
    attribute_name = request.GET.get('attribute_name', '').strip()
    offset = request.GET.get("offset", None)
    limit = request.GET.get('limit', None)
    # If no attribute is specified, return an error message or all data as fallback
    if not attribute_name:
        return Response({"error": "No attribute_name specified."}, status=400)

    # Define a list of valid attributes (column names) to prevent any unexpected column access
    valid_attributes = [
        'PATENT_OWNER',
        'Sub_Technology',
        'Publication_Number',
        'Current_Assignee',
        'Application_Number',
        'RECOMMENDATION',
        'Inventor',
        'IPRD_REFERENCE',
        'Patent_Number'
    ]

    # Check if the attribute_name is valid
    if attribute_name not in valid_attributes:
        return Response({"error": f"Invalid attribute_name: {attribute_name}."}, status=400)

    # Fetch the distinct values for the given attribute from the database
    data = Sep_Search.objects.exclude(**{attribute_name: ''}).values_list(attribute_name, flat=True).distinct()
    # data = Sep_Search.objects.values_list(attribute_name, flat=True).distinct()
    if offset is not None and limit is not None:
        offset, limit = int(offset), int(limit)
        return Response({attribute_name: data[offset:offset + limit]})
    else:
        return Response({attribute_name: data})
    # Return the distinct values for the attribute
    # return Response({attribute_name: list(data)})

# def unique_data(request):
#     attribute_name=request.GET.get('attribute_name', '')
#     data = Sep_Search.objects.find_all()
#     count = {
#         'PATENT_OWNER': list(data.values_list('PATENT_OWNER', flat=True).distinct()),
#         'Sub_Technology': list(data.values_list('Sub_Technology', flat=True).distinct()),
#         'Publication_Number': list(data.values_list('Publication_Number', flat=True).distinct()),
#         'Current_Assignee': list(data.values_list('Current_Assignee', flat=True).distinct()),
#         'Application_Number': list(data.values_list('Application_Number', flat=True).distinct()),
#         'RECOMMENDATION': list(data.values_list('RECOMMENDATION', flat=True).distinct()),
#         'Inventor': list(data.values_list('Inventor', flat=True).distinct()),
#         'IPRD_REFERENCE':list(data.values_list('IPRD_REFERENCE', flat=True).distinct())
#
#     }
#     return Response({"result": count})

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_limit(request):
    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)
    user_profile = request.user.userprofile
    if user_profile.search_count < 5:
        # Perform the search here (for example, search for a query in the request)
        user_profile.search_count += 1
        user_profile.save()
        return Response({"search_count":str(user_profile.search_count)})
    else:
        return Response({"message":"Free limit exhausted reach insidesep@patentskart.com for complete access","status":"False"})

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def database_count(request):
    tech = request.GET.getlist("TECH[]", [])
    stand_sett = request.GET.getlist("STANDARD_SET[]", [])
    patent = request.GET.getlist("PATENT_OWNER[]", [])
    stand = request.GET.getlist("STANDARD[]", [])
    IPRD_REF = request.GET.getlist('IPRD_REFERENCE[]', [])
    Patent_num = request.GET.getlist('PATENT_NUM[]', [])
    Sub_Technology = request.GET.getlist('Sub_Tech[]', [])
    from_date = request.GET.get('DATE_FROM', '')
    to_date = request.GET.get('DATE_TO', '')
    offset = request.GET.get("offset", None)
    limit = request.GET.get('limit', None)

    # Initialize empty Q object to accumulate conditions
    query = Q()
    # Append conditions dynamically based on inputs
    if tech:
        tech_query = Q()  # Start with an empty Q object for tech
        for tec in tech:
            tech_query |= Q(Technology__icontains=tec)  # Use |= to accumulate OR conditions
        query &= tech_query  # Add the accumulated tech conditions to the main query
    if stand_sett:
        query &= Q(STANDARD_SETTING__in=stand_sett)
    if patent:
        query &= Q(PATENT_OWNER__in=patent)
    if stand:
        query &= Q(STANDARD__in=stand)
    if IPRD_REF:
        query &= Q(IPRD_REFERENCE__in=IPRD_REF)
    if Patent_num:
        query &= Q(Patent_Number__in=Patent_num)
    if Sub_Technology:
        query &= Q(Sub_Technology__in=Sub_Technology)
    if from_date and to_date:
        query &= Q(IPRD_SIGNATURE_DATE__gte=from_date) & Q(IPRD_SIGNATURE_DATE__lte=to_date)

    # Apply filters
    data = Sep_dashboard.objects.filter(query) if query else Sep_dashboard.objects.filter(STANDARD__iexact="ahhh")

    # Distinct on IPRD_REFERENCE and serialize results
    data1 = data.distinct('IPRD_REFERENCE')
    unique_res = Sep_dashboard_Serilizaer(data1, many=True)

    # Count distinct values for each category
    count = {
        'Inventor': data.values('Inventor').distinct().count(),
        'PATENT_OWNER': data.values('PATENT_OWNER').distinct().count(),
        'Publication_Number': data.values('Publication_Number').distinct().count(),
        'SSO': data.values('STANDARD_SETTING').distinct().count(),
        'STANDARD': data.values('STANDARD').distinct().count(),
        'Sub_Technology': data.values('Sub_Technology').distinct().count(),
        'Technology': data.values('Technology').distinct().count()
    }
    count_data = {'total': data.count(), 'cat_count': count}

    # Paginate results if offset and limit are provided
    if offset is not None and limit is not None:
        offset, limit = int(offset), int(limit)
        return Response({'result': unique_res.data[offset:offset + limit], 'count': count_data})
    else:
        return Response({'result': unique_res.data, 'count': count_data})


# def database_count(request):
#     tech=request.GET.getlist("TECH[]",[])
#     stand_sett=request.GET.getlist("STANDARD_SET[]",[])
#     patent=request.GET.getlist("PATENT_OWNER[]",[])
#     stand=request.GET.getlist("STANDARD[]",[])
#     IPRD_REF=request.GET.getlist('IPRD_REFERENCE[]',[])
#     Patent_num =request.GET.get('PATENT_NUM', '')
#     Sub_Technology=request.GET.getlist('Sub_Tech[]', [])
#     from_date=request.GET.get('DATE_FROM','')
#     to_date = request.GET.get('DATE_TO','')
#     offset = request.GET.get("offset", None)
#     limit =  request.GET.get('limit', None)
#     if len(tech)>0:
#         query = Q()
#         for tec in tech:
#             query |= Q(Technology__icontains=tec)
#
#     if len(tech)==0 and len(stand_sett)==0 and len(patent)==0 and len(stand)==0 and len(IPRD_REF)==0 and Patent_num=='' and len(Sub_Technology)==0 and from_date=="" and to_date =="":
#         data = Sep_dashboard.objects.filter(STANDARD__iexact="ahhh")
#
#     elif from_date!="" and to_date!="" and len(stand_sett)>0 and len(tech)>0 and len(stand_sett)==0 and len(patent)==0 and len(stand)==0 and len(IPRD_REF)==0:
#         data = Sep_dashboard.objects.filter(query
#                                             & Q(STANDARD__in=stand)
#                                             & Q(STANDARD_SETTING__in=stand_sett)
#                                             & Q(PATENT_OWNER__in=patent)
#                                             & Q(IPRD_REFERENCE__in=IPRD_REF)
#                                             & Q(Patent_Number__icontains=Patent_num)
#                                             & Q(Sub_Technology__in=Sub_Technology)
#                                             & Q(IPRD_SIGNATURE_DATE__gte=from_date)
#                                             & Q(IPRD_SIGNATURE_DATE__lte=to_date))
#     elif from_date!="" and to_date!="" and len(stand_sett)>0:
#         data = Sep_dashboard.objects.filter(Q(STANDARD_SETTING__in=stand_sett)
#                                             & Q(STANDARD__icontains=stand)
#                                             & Q(PATENT_OWNER__icontains=patent)
#                                             & Q(IPRD_REFERENCE__icontains=IPRD_REF)
#                                             & Q(Patent_Number__icontains=Patent_num)
#                                             & Q(Sub_Technology__icontains=Sub_Technology)
#                                             & Q(IPRD_SIGNATURE_DATE__gte=from_date)
#                                             & Q(IPRD_SIGNATURE_DATE__lte=to_date))
#     elif from_date!="" and to_date!="" and len(tech)>0:
#         data = Sep_dashboard.objects.filter(query
#                                             & Q(STANDARD__icontains=stand)
#                                             & Q(PATENT_OWNER__icontains=patent)
#                                             & Q(IPRD_REFERENCE__icontains=IPRD_REF)
#                                             & Q(Patent_Number__icontains=Patent_num)
#                                             & Q(Sub_Technology__icontains=Sub_Technology)
#                                             & Q(IPRD_SIGNATURE_DATE__gte=from_date)
#                                             & Q(IPRD_SIGNATURE_DATE__lte=to_date))
#     elif len(stand_sett)>0 and len(tech)>0:
#         data = Sep_dashboard.objects.filter(query
#                                             & Q(STANDARD_SETTING__in=stand_sett)
#                                             & Q(STANDARD__icontains=stand)
#                                             & Q(PATENT_OWNER__icontains=patent)
#                                             & Q(IPRD_REFERENCE__icontains=IPRD_REF)
#                                             & Q(Patent_Number__icontains=Patent_num)
#                                             & Q(Sub_Technology__icontains=Sub_Technology))
#     elif len(stand_sett)>0:
#         data = Sep_dashboard.objects.filter(Q(STANDARD_SETTING__in=stand_sett) &
#                                             Q(STANDARD__icontains=stand) &
#                                             Q(PATENT_OWNER__in=patent) &
#                                             Q(IPRD_REFERENCE__icontains=IPRD_REF)&
#                                             Q(Patent_Number__icontains=Patent_num)&
#                                             Q(Sub_Technology__icontains=Sub_Technology))
#     elif len(tech)>0:
#         data = Sep_dashboard.objects.filter(query
#                                             & Q(STANDARD__icontains=stand)
#                                             & Q(PATENT_OWNER__icontains=patent)
#                                             & Q(IPRD_REFERENCE__icontains=IPRD_REF)
#                                             & Q(Patent_Number__icontains=Patent_num)
#                                             & Q(Sub_Technology__icontains=Sub_Technology))
#     elif from_date!="" and to_date!="":
#         data = Sep_dashboard.objects.filter(Q(STANDARD__icontains=stand)
#                                             & Q(PATENT_OWNER__icontains=patent)
#                                             & Q(IPRD_REFERENCE__icontains=IPRD_REF)
#                                             & Q(Patent_Number__icontains=Patent_num)
#                                             & Q(Sub_Technology__icontains=Sub_Technology)
#                                             & Q(IPRD_SIGNATURE_DATE__gte=from_date)
#                                             & Q(IPRD_SIGNATURE_DATE__lte=to_date))
#     else:
#         data = Sep_dashboard.objects.filter(Q(STANDARD__icontains=stand)
#                                             & Q(PATENT_OWNER__icontains=patent)
#                                             & Q(IPRD_REFERENCE__icontains=IPRD_REF)
#                                             & Q(Patent_Number__icontains=Patent_num)
#                                             & Q(Sub_Technology__icontains=Sub_Technology))
#     data1 = data.distinct('IPRD_REFERENCE')
#     unique_res = Sep_dashboard_Serilizaer(data1, many=True)
#     # res = Sep_dashboard_Serilizaer(data, many=True)
#     count = {'Inventor': '', 'PATENT_OWNER': '', 'Publication_Number': '', 'SSO': '', 'STANDARD': '',
#              'Sub_Technology': '',
#              'Technology': ''}
#     try:
#         count['SSO'] = data.values('STANDARD_SETTING').distinct().count()
#         count['STANDARD'] = data.values('STANDARD').distinct().count()
#         count['Technology'] = data.values('Technology').distinct().count()
#         count['PATENT_OWNER'] = data.values('PATENT_OWNER').distinct().count()
#         count['Sub_Technology'] = data.values('Sub_Technology').distinct().count()
#         count['Publication_Number'] = data.values('Publication_Number').distinct().count()
#         count['Inventor'] = data.values('Inventor').distinct().count()
#         count_data = {'total': data.count(), 'cat_count': count}
# #     return JsonResponse(result)
#     except Exception as e:
#         count_data = {'total': 0, 'cat_count': count}
#         # return JsonResponse(result)
#     # count_data= evaluate_data(res)
#     if offset is not None and limit is not None:
#         offset = int(offset)
#         limit = int(limit)
#         return Response({'result':unique_res.data[offset:offset+limit],'count':count_data})
#     else:
#         return Response({'result': unique_res.data, 'count': count_data})

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

FREE_EMAIL_DOMAINS = [
    'gmail.com', 'yahoo.com', 'yopmail.com', 'hotmail.com', 'aol.com', 'icloud.com', 'yandex.com'
]

def is_business_email(email):
    """ Check if the email domain is not a free email provider """
    domain = email.split('@')[-1]  # Extract domain from email
    return domain not in FREE_EMAIL_DOMAINS


@api_view(['POST'])
def signup(request):
    # Get the email from request data
    email = request.data.get('email', '')

    # Check if the email is a valid business email (not from free email providers)
    if not is_business_email(email):
        return Response("Please use a valid business email address.",
                        status=status.HTTP_400_BAD_REQUEST)

    # Proceed with the regular serializer logic if email is valid
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Save the new user data
        serializer.save()

        # Get the created user object
        user = User.objects.get(username=request.data['username'])

        # Set the password for the user
        user.set_password(request.data['password'])
        user.save()

        # Generate a token for the user
        token = Token.objects.create(user=user)

        # Return the token and user data
        return Response({"token": token.key, "user": serializer.data})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def signup(request):
#     serilizer= UserSerializer(data=request.data)
#     if serilizer.is_valid():
#         serilizer.save()
#         user=User.objects.get(username=request.data['username'])
#         user.set_password(request.data['password'])
#         user.save()
#         token=Token.objects.create(user=user)
#         return Response({"token":token.key,"user":serilizer.data})
#     return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

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