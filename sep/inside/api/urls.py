# from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path,include
from .views import database_view,patents_view,database_count,get_database,PatentsAutocomplete,unique_data
from .views import signup,login,test_token

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("list/",database_view),
    # path("list1/",dashboard_search.as_view()),
    path("<int:pk>",patents_view),
    path('signup/',signup),
    path('login/',login),
    path('test_token/',test_token),
    path('search/',database_count),
    path('search_iprd/',get_database),
    path('patents-autocomplete/', PatentsAutocomplete.as_view(), name='country-autocomplete'),
    path('unique_data',unique_data)
]