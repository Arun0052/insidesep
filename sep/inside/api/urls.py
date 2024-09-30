# from django.contrib import admin
from django.urls import path,include
from .views import database_view,patents_view,database_count,get_database
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
    path('search_iprd/',get_database)
]