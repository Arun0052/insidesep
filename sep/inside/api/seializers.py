from rest_framework import serializers
from ..models import Sep_dashboard,Sep_Search
from django.contrib.auth.models import User

class Sep_dashboard_Serilizaer(serializers.Serializer):
    S_No = serializers.CharField(required=False, allow_null=True)
    id=serializers.IntegerField(read_only=True)
    S_No = serializers.CharField(allow_blank=True)
    STANDARD_SETTING = serializers.CharField(allow_blank=True)
    IPRD_REFERENCE = serializers.CharField(allow_blank=True)
    DIPG_DISPLAY_NUMBER = serializers.IntegerField()
    IPRD_SIGNATURE_DATE = serializers.DateField()
    PATENT_OWNER = serializers.CharField(allow_blank=True)
    Current_Assignee = serializers.CharField(allow_blank=True)
    STANDARD = serializers.CharField(allow_blank=True)
    ILLUSTRATIVE_PART = serializers.CharField(allow_blank=True)
    Ess_To_Project = serializers.BooleanField()
    Ess_To_Standard = serializers.BooleanField()
    # Ess_To_Project=serializers.CharField(allow_blank=True)
    # Ess_To_Standard=serializers.CharField(allow_blank=True)
    App_pub_pat_Number = serializers.CharField(allow_blank=True)
    Application_Number = serializers.CharField(allow_blank=True)
    Publication_Number = serializers.CharField(allow_blank=True)
    Patent_Number = serializers.CharField(allow_blank=True)
    COUNTRY_CODE = serializers.CharField(allow_blank=True)
    Type = serializers.CharField(allow_blank=True)
    DIPG_EXTERNAL_ID = serializers.CharField(allow_blank=True)
    COMMITTEE = serializers.CharField(allow_blank=True)
    RECOMMENDATION = serializers.CharField(allow_blank=True)
    Technology = serializers.CharField(allow_blank=True)
    Sub_Technology = serializers.CharField(allow_blank=True)
    Title = serializers.CharField(allow_blank=True)
    DIPG_ID = serializers.IntegerField()
    DIPG_PATF_ID = serializers.IntegerField()
    PATT_ID = serializers.IntegerField()
    Inventor = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        return Sep_dashboard.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.S_No = validated_data.get('S_No',instance.S_No)
        instance.STANDARD_SETTING = validated_data.get('STANDARD_SETTING',instance.STANDARD_SETTING)
        instance.IPRD_REFERENCE = validated_data.get('IPRD_REFERENCE',instance.IPRD_REFERENCE)
        instance.DIPG_DISPLAY_NUMBER = validated_data.get('DIPG_DISPLAY_NUMBER',instance.DIPG_DISPLAY_NUMBER)
        instance.IPRD_SIGNATURE_DATE = validated_data.get('IPRD_SIGNATURE_DATE',instance.IPRD_SIGNATURE_DATE)
        instance.PATENT_OWNER = validated_data.get('PATENT_OWNER',instance.PATENT_OWNER)
        instance.Current_Assignee = validated_data.get('ETPR_ACRONYM',instance.Current_Assignee)
        instance.STANDARD = validated_data.get('STANDARD',instance.STANDARD)
        instance.ILLUSTRATIVE_PART = validated_data.get('ILLUSTRATIVE_PART',instance.ILLUSTRATIVE_PART)
        instance.Ess_To_Project = validated_data.get('Ess_To_Project',instance.Ess_To_Project)
        instance.Ess_To_Standard = validated_data.get('Ess_To_Standard',instance.Ess_To_Standard)
        instance.App_pub_pat_Number = validated_data.get('App_pub_pat_Number',instance.App_pub_pat_Number)
        instance.Application_Number = validated_data.get('Application_Number',instance.Application_Number)
        instance.Publication_Number = validated_data.get('Publication_Number',instance.Publication_Number)
        instance.Patent_Number = validated_data.get('Patent_Number',instance.Patent_Number)
        instance.COUNTRY_CODE = validated_data.get('COUNTRY_CODE',instance.COUNTRY_CODE)
        instance.Type = validated_data.get('Tye',instance.Type)
        instance.DIPG_EXTERNAL_ID = validated_data.get('DIPG_EXTERNAL_ID',instance.DIPG_EXTERNAL_ID)
        instance.COMMITTEE = validated_data.get('COMMITTEE',instance.COMMITTEE)
        instance.RECOMMENDATION = validated_data.get('RECOMMENDATION',instance.RECOMMENDATION)
        instance.Technology = validated_data.get('Technology',instance.Technology)
        instance.Sub_Technology = validated_data.get('Sub_Technology',instance.Sub_Technology)
        instance.Title = validated_data.get('Title',instance.Title)
        instance.DIPG_ID = validated_data.get('DIPG_ID',instance.DIPG_ID)
        instance.DIPG_PATF_ID = validated_data.get('DIPG_PATF_ID',instance.DIPG_PATF_ID)
        instance.PATT_ID = validated_data.get('PATT_ID',instance.PATT_ID)
        instance.Inventor = validated_data.get('Inventor',instance.Inventor)
        instance.save()
        return instance


class Sep_search_Serilizaer(serializers.Serializer):
    IPRD_REFERENCE = serializers.CharField(allow_blank=True)
    PATENT_OWNER = serializers.CharField(allow_blank=True)
    Current_Assignee = serializers.CharField(allow_blank=True)
    Application_Number = serializers.CharField(allow_blank=True)
    Publication_Number = serializers.CharField(allow_blank=True)
    RECOMMENDATION = serializers.CharField(allow_blank=True)
    Sub_Technology = serializers.CharField(allow_blank=True)
    Inventor = serializers.CharField(allow_blank=True)
    Patent_Number = serializers.CharField(allow_null=True)

    def create(self, validated_data):
        return Sep_Search.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=User
        fields=['id','username','password','email']


# serializers.py

# from rest_framework import serializers

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

# serializers.py

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
