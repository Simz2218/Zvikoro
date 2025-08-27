import re
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import viewsets

from .models import (
    Admin, Users,
    PSchool, SSchool,
    PGradeEnrollment, SGradeEnrollment,
    PTeacherData, STeacherData,
    PryPayments, SecPayments, Messages
)
from .utils import validate_excel_file_extension


# -------------------------
# JWT Token Serializer
# -------------------------

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ["first_name", "surname", "department", "phone_number"]


import logging

logger = logging.getLogger(__name__)  # You can configure this in settings.py

class UserProfileSerializer(serializers.ModelSerializer):
    admin = AdminProfileSerializer(required=False)
    profile = serializers.ImageField(required=False)
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ["id", "username", "email", "profile", "profile_url", "bio", "is_admin", "admin"]
        extra_kwargs = {
            "profile": {"required": False}
        }

    def get_profile_url(self, obj):
        request = self.context.get("request")
        return obj.get_profile_url(request)

    def update(self, instance, validated_data):
        logger.info(f"Incoming validated_data: {validated_data}")

        admin_data = validated_data.pop("admin", None)
        logger.info(f"Extracted admin_data: {admin_data}")

        # Handle profile image separately
        if "profile" in validated_data:
            profile_file = validated_data.pop("profile")
            if profile_file is None:
                logger.info("Removing profile image")
                instance.profile.delete(save=False)
                instance.profile = None
            else:
                logger.info(f"Updating profile image: {profile_file}")
                instance.profile = profile_file
        else:
            logger.info("No profile image provided")

        # Update user fields
        for attr, value in validated_data.items():
            logger.info(f"Updating user field: {attr} = {value}")
            setattr(instance, attr, value)
        instance.save()
        logger.info(f"User {instance.username} saved successfully")

        # Update or create nested admin
        if admin_data:
            if instance.admin:
                logger.info(f"Updating existing admin for user {instance.username}")
                for attr, value in admin_data.items():
                    logger.info(f"Updating admin field: {attr} = {value}")
                    setattr(instance.admin, attr, value)
                instance.admin.save()
            else:
                logger.info(f"Creating new admin for user {instance.username}")
                admin_obj = Admin.objects.create(**admin_data)
                instance.admin = admin_obj
                instance.save()

        return instance



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # ✅ Pass request context to serializer
        request = self.context.get("request")
        user_data = UserProfileSerializer(self.user, context={"request": request}).data

        # ✅ Only include user object in response
        data['user'] = user_data
        return data


# -------------------------
# Admin Creation Serializer
# -------------------------
class AdminCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ["phone_number", "first_name", "surname", "department",]

    def validate_phone_number(self, value):
        if not re.fullmatch(r"^\d{10}$", value):
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        if Admin.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("An Admin with this phone number already exists.")
        return value

    def validate_first_name(self, value):
        if not value.isalpha() or len(value) < 2:
            raise serializers.ValidationError("First name must be at least 2 letters and contain only letters.")
        return value.title()

    def validate_surname(self, value):
        if not value.isalpha() or len(value) < 2:
            raise serializers.ValidationError("Surname must be at least 2 letters and contain only letters.")
        return value.title()

    def validate_department(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Department name is too short.")
        return value.strip().title()


# -------------------------
# Linked User Creation (Admin must exist)
# -------------------------


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Users
        fields = ["admin", "username", "email", "password", "password2", "is_admin"]

    def validate(self, data):
        # Only enforce password match if either password field is provided
        if "password" in data or "password2" in data:
            if data.get("password") != data.get("password2"):
                raise serializers.ValidationError("Passwords must match.")

        # Only resolve admin phone number if 'admin' is provided in request
        if "admin" in self.initial_data:
            try:
                data["admin"] = Admin.objects.get(phone_number=self.initial_data["admin"])
            except Admin.DoesNotExist:
                raise serializers.ValidationError(
                    "No Admin with this phone number exists. Please create the Admin first."
                )

        # Only check username uniqueness on create or if username is being changed
        if self.instance is None or ("username" in data and data["username"] != getattr(self.instance, "username", None)):
            if Users.objects.filter(username=data["username"]).exists():
                raise serializers.ValidationError("Username already taken.")

        return data

    def create(self, validated_data):
        validated_data.pop("password2", None)
        pwd = validated_data.pop("password", None)
        user = Users(**validated_data)
        if pwd:
            user.set_password(pwd)
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop("password2", None)
        pwd = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if pwd:
            instance.set_password(pwd)

        instance.save()
        return instance


# -------------------------
# Profile Serializers
# -------------------------
class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ["phone_number", "first_name", "surname", "department"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "username", "email", "is_admin", "profile", "bio", "admin","department"]


# serializers.py


class UserProfileSerializer(serializers.ModelSerializer):
    admin = AdminProfileSerializer(required=False)
    profile = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()  # ✅ Flattened department

    class Meta:
        model = Users
        fields = ["id", "username", "email", "profile", "bio", "is_admin", "admin", "department"]
        extra_kwargs = {
            "profile": {"required": False}
        }

    def get_profile(self, obj):
        request = self.context.get("request")
        if obj.profile:
            return request.build_absolute_uri(obj.profile.url)
        return None

    def get_department(self, obj):
        if obj.admin:
            return obj.admin.department
        return None

    def update(self, instance, validated_data):
        admin_data = validated_data.pop("admin", None)

        if "profile" in validated_data:
            profile_file = validated_data.pop("profile")
            if profile_file is None:
                instance.profile.delete(save=False)
                instance.profile = None
            else:
                instance.profile = profile_file

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if admin_data:
            if instance.admin:
                for attr, value in admin_data.items():
                    setattr(instance.admin, attr, value)
                instance.admin.save()
            else:
                admin_obj = Admin.objects.create(**admin_data)
                instance.admin = admin_obj
                instance.save()

        return instance


# -------------------------
# File Upload Serializers
# -------------------------
class ExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[validate_excel_file_extension])

    def validate_file(self, f):
        if f.size > 5 * 1024 * 1024:
            raise ValidationError("Max size 5MB.")
        return f


class CSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()


# -------------------------
# School & Data Serializers
# -------------------------
class PSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSchool
        fields = "__all__"


class SSchoolSerializer(PSchoolSerializer):
    class Meta(PSchoolSerializer.Meta):
        model = SSchool


class PGradeEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PGradeEnrollment
        fields = "__all__"


class SGradeEnrollmentSerializer(PGradeEnrollmentSerializer):
    class Meta(PGradeEnrollmentSerializer.Meta):
        model = SGradeEnrollment


class PTeacherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PTeacherData
        fields = "__all__"


class STeacherDataSerializer(PTeacherDataSerializer):
    class Meta(PTeacherDataSerializer.Meta):
        model = STeacherData


# -------------------------
# Payment Serializers
# -------------------------
import datetime
from rest_framework import serializers
from .models import PSchool, PryPayments, PGradeEnrollment

class PryPaymentSerializer(serializers.ModelSerializer):
    # Always returned in responses, never required in requests
    school_name = serializers.SerializerMethodField(read_only=True)

    # Accept either a school ID or nothing
    school = serializers.PrimaryKeyRelatedField(
        queryset=PSchool.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = PryPayments
        fields = [
            'id', 'school', 'school_name',
            'paid_amount', 'date_paid',
            'balance', 'year', 'term'
        ]
        read_only_fields = ['balance', 'year', 'term']

    def get_school_name(self, obj):
        return obj.school.name if obj.school else None

    def validate(self, data):
        # If no school provided, you can decide whether to allow or block
        school = data.get('school')
        if not school:
            raise serializers.ValidationError({
                "school": "Please select a school."
            })

        if PryPayments.objects.filter(
            school=school,
            paid_amount=data['paid_amount'],
            date_paid=data['date_paid']
        ).exists():
            raise serializers.ValidationError(
                "A payment with the same amount and date already exists for this school."
            )
        return data

    def create(self, validated_data):
        current_year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        current_term = (
            1 if month in [1, 2, 3, 4]
            else 2 if month in [5, 6, 7, 8]
            else 3
        )

        school = validated_data.pop('school', None)
        last_payment = PryPayments.objects.filter(school=school).order_by('-id').first()
        opening_balance = last_payment.balance if last_payment else 0
        balance = opening_balance + validated_data['paid_amount']

        return PryPayments.objects.create(
            school=school,
            paid_amount=validated_data['paid_amount'],
            date_paid=validated_data['date_paid'],
            year=current_year,
            term=current_term,
            balance=balance
        )



# serializers.py
from .models import SSchool, SecPayments, SGradeEnrollment

class SecPaymentSerializer(serializers.ModelSerializer):
    # Always returned in responses, never required in requests
    school_name = serializers.SerializerMethodField(read_only=True)

    # Accept a school ID from the frontend
    school = serializers.PrimaryKeyRelatedField(
        queryset=SSchool.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = SecPayments
        fields = [
            'id', 'school', 'school_name',
            'paid_amount', 'date_paid',
            'balance', 'year', 'term'
        ]
        read_only_fields = ['balance', 'year', 'term']

    def get_school_name(self, obj):
        return obj.school.name if obj.school else None

    def validate(self, data):
        school = data.get('school')
        if not school:
            raise serializers.ValidationError({
                "school": "Please select a school."
            })

        if SecPayments.objects.filter(
            school=school,
            paid_amount=data['paid_amount'],
            date_paid=data['date_paid']
        ).exists():
            raise serializers.ValidationError(
                "A payment with the same amount and date already exists for this school."
            )
        return data

    def create(self, validated_data):
        current_year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        current_term = (
            1 if month in [1, 2, 3, 4]
            else 2 if month in [5, 6, 7, 8]
            else 3
        )

        school = validated_data.pop('school', None)
        last_payment = SecPayments.objects.filter(school=school).order_by('-id').first()
        opening_balance = last_payment.balance if last_payment else 0
        balance = opening_balance + validated_data['paid_amount']

        return SecPayments.objects.create(
            school=school,
            paid_amount=validated_data['paid_amount'],
            date_paid=validated_data['date_paid'],
            year=current_year,
            term=current_term,
            balance=balance
        )


class PryPaymentsListSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = PryPayments
        fields = [
            'id',
            'school',        # FK ID
            'school_name',   # Human-readable name
            'paid_amount',
            'date_paid',
            'year',
            'term',
            'balance'
        ]



class SecPaymentsListSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = SecPayments
        fields = [
            'id',
            'school',        # FK ID
            'school_name',   # Human-readable name
            'paid_amount',
            'date_paid',
            'year',
            'term',
            'balance'
        ]
        
# serializers.py


class PublicMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    department = serializers.CharField(source='user.department', read_only=True)

    class Meta:
        model = Messages
        fields = ['id', 'username', 'profile_picture', 'department', 'message']


# serializers.py

class MessageSerializer(serializers.ModelSerializer):
    department = serializers.CharField(read_only=True)
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Messages
        fields = ['id', 'message', 'department', 'sender']
        read_only_fields = ['department', 'sender']

    def get_sender(self, obj):
        return obj.user.username
