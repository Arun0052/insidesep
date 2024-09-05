# from django.contrib import admin
from django.urls import path,include
from .views import database_view,patents_view
from .views import signup,login

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("list/",database_view),
    path("<int:pk>",patents_view),
    path('signup/',signup),
    path('login/',login)
]