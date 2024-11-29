from django.db import models

# Create your models here.

# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Sep_Search(models.Model):
    IPRD_REFERENCE=models.CharField(max_length=1000,blank=True)
    PATENT_OWNER=models.CharField(max_length=1000,blank=True)
    Current_Assignee=models.CharField(max_length=1000,blank=True)
    Application_Number=models.CharField(max_length=1000,blank=True)
    Publication_Number=models.CharField(max_length=1000,blank=True)
    RECOMMENDATION=models.CharField(max_length=1000,blank=True)
    Sub_Technology=models.CharField(max_length=1000,blank=True)
    Inventor=models.CharField(max_length=1000,blank=True)
    Patent_Number=models.CharField(max_length=1000,blank=True)
    def __str__(self):
        return self.Application_Number


class Sep_dashboard(models.Model):
    S_No=models.CharField(max_length=20,blank=True)
    STANDARD_SETTING=models.CharField(max_length=200,blank=True)
    IPRD_REFERENCE=models.CharField(max_length=1000,blank=True)
    DIPG_DISPLAY_NUMBER=models.IntegerField(blank=True)
    IPRD_SIGNATURE_DATE=models.DateField(blank=True)
    PATENT_OWNER=models.CharField(max_length=1000,blank=True)
    Current_Assignee=models.CharField(max_length=1000,blank=True)
    STANDARD=models.CharField(max_length=1000,blank=True)
    ILLUSTRATIVE_PART=models.CharField(max_length=1000,blank=True)
    Ess_To_Project=models.BooleanField(default=False)
    Ess_To_Standard=models.BooleanField(default=False)
    # Ess_To_Project=models.CharField(max_length=1000,blank=True)
    # Ess_To_Standard=models.CharField(max_length=1000,blank=True)
    App_pub_pat_Number=models.CharField(max_length=1000,blank=True)
    Application_Number=models.CharField(max_length=1000,blank=True)
    Publication_Number=models.CharField(max_length=1000,blank=True)
    Patent_Number=models.CharField(max_length=1000,blank=True)
    COUNTRY_CODE=models.CharField(max_length=1000,blank=True)
    Type=models.CharField(max_length=1000,blank=True)
    DIPG_EXTERNAL_ID=models.CharField(max_length=1000,blank=True)
    COMMITTEE=models.CharField(max_length=1000,blank=True)
    RECOMMENDATION=models.CharField(max_length=1000,blank=True)
    Technology=models.CharField(max_length=1000,blank=True)
    Sub_Technology=models.CharField(max_length=1000,blank=True)
    Title=models.CharField(max_length=1000,blank=True)
    DIPG_ID=models.IntegerField(blank=True)
    DIPG_PATF_ID=models.IntegerField(blank=True)
    PATT_ID=models.IntegerField(blank=True)
    Inventor=models.CharField(max_length=1000,blank=True)

    def __str__(self):
        return self.S_No

