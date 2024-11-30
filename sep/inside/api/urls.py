# from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path,include
from .views import search_view,database_view,patents_view,database_count,get_database,PatentsAutocomplete,search_by_attribute
from .views import signup,login,test_token,user_limit
from .views import PasswordResetRequestView, PasswordResetConfirmView
from django.urls import path
from .views import ResetSearchCountAPIView

# myapp/urls.py


#added two end points
urlpatterns = [
    path("list/",database_view),
    path("list_search/", search_view),
    path("<int:pk>",patents_view),
    path('signup/',signup),
    path('login/',login),
    path('test_token/',test_token),
    path('search/',database_count),
    path('search_iprd/',get_database),
    path('patents-autocomplete/', PatentsAutocomplete.as_view(), name='country-autocomplete'),
    path("user_limit/", user_limit),
    path('reset-userlimit/', ResetSearchCountAPIView),
    path('search_by_attribute/',search_by_attribute),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
# urls.py

