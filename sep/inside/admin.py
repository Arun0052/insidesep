from .models import Sep_dashboard
from django.contrib import admin
from .models import ExcludedUser


@admin.register(ExcludedUser)
class ExcludedUserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username',)



admin.site.register(Sep_dashboard)



