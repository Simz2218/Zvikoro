from schools.models import Admin,  Users, PSchool, PGradeEnrollment, PTeacherData,SSchool, SGradeEnrollment, STeacherData, PryPayments, SecPayments

from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers 
from django.core.exceptions import ObjectDoesNotExist
import logging
import os
from rest_framework.exceptions import ValidationError
import datetime


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Users
        fields = '__all__'






from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

logger = logging.getLogger(__name__)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims from Users and related Admin
        token['username'] = user.username
        if user.admin:
            token['first_name'] = user.admin.first_name
            token['surname'] = user.admin.surname
            token['department'] = user.admin.department
        else:
            token['first_name'] = ''
            token['surname'] = ''
            token['department'] = ''

        return token

class AdminUserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ['admin', 'username', 'password', 'password2', 'email']

    def validate(self, attrs):
    # Check if passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields don't match."})

        admin_phone = self.initial_data.get('admin')  # Get raw phone number from input
        username = attrs.get('username')

        try:
            admin_instance = Admin.objects.get(phone_number=admin_phone)
            attrs['admin'] = admin_instance  # Inject resolved Admin object into validated data
        except Admin.DoesNotExist:
            raise serializers.ValidationError({"admin": "Admin with this phone number does not exist."})

        if Users.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})

        return attrs


    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = Users(**validated_data)
        user.set_password(password)
        user.save()
        return user


    
class EmployeeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = [ 'first_name', 'surname', 'department', 'phone_number',]

    def validate(self, attrs):
        if Admin.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "Admin with this phone_number already exists."})
        if Admin.objects.filter(first_name=attrs['first_name'], surname=attrs['surname']).exists():
            raise serializers.ValidationError({"first_name": "Admin with this name already exists."})
        return attrs

    def create(self, validated_data):
        return Admin.objects.create(**validated_data)





    

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


####




def validate_excel_file(value):
    allowed_extensions = ['.xls', '.xlsx']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in allowed_extensions:
        raise ValidationError(f'Invalid file type: {ext}. Only Excel files are allowed: {", ".join(allowed_extensions)}.')

class ExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[validate_excel_file])

    # Optional: Add a file size validation
    def validate_file(self, value):
        max_size = 5 * 1024 * 1024  # 5 MB limit
        if value.size > max_size:
            raise ValidationError('File size exceeds the maximum limit of 5 MB.')
        return value



class PSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSchool
        fields = '__all__'

class PGradeEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PGradeEnrollment
        fields = '__all__'

class PTeacherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PTeacherData
        fields = '__all__'
        
        
        
def validate_excel_file(value):
    allowed_extensions = ['.xls', '.xlsx']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in allowed_extensions:
        raise ValidationError(f'Invalid file type: {ext}. Only Excel files are allowed: {", ".join(allowed_extensions)}.')

class SecondaryExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[validate_excel_file])

    # Optional: Add a file size validation
    def validate_file(self, value):
        max_size = 5 * 1024 * 1024  # 5 MB limit
        if value.size > max_size:
            raise ValidationError('File size exceeds the maximum limit of 5 MB.')
        return value



class SSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSchool
        fields = '__all__'

class SGradeEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SGradeEnrollment
        fields = '__all__'

class STeacherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = STeacherData
        fields = '__all__'


class CSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

class PryPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PryPayments
        fields = ['id', 'school', 'paid_amount','date_paid', 'balance', 'year', 'term']

class SecPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecPayments
        fields = ['id', 'school', 'paid_amount','date_paid', 'balance', 'year', 'term']

class SecPaymentSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(max_length=255, write_only=True)
    school = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SecPayments
        fields = ['id', 'school', 'school_name', 'paid_amount', 'date_paid']

    def validate_school_name(self, value):
        try:
            school = SSchool.objects.get(name__iexact=value)
            return school.id
        except SSchool.DoesNotExist:
            raise serializers.ValidationError("School does not exist.")

    def create(self, validated_data):
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        if current_month in [1, 2, 3, 4]:
            current_term = 1
        elif current_month in [5, 6, 7, 8]:
            current_term = 2
        else:
            current_term = 3

        school_id = validated_data.pop('school_name')
        last_payment = SecPayments.objects.filter(school_id=school_id).order_by('-id').first()
        if last_payment:
            balance = last_payment.balance + validated_data['paid_amount']
        else:
            balance = validated_data['paid_amount']

        return SecPayments.objects.create(
            school_id=school_id,
            paid_amount=validated_data['paid_amount'],
            date_paid=validated_data['date_paid'],
            year=current_year,
            term=current_term,
            balance=balance
        )

    def validate(self, data):
        school_id = data.get('school_name')
        existing_payment = SecPayments.objects.filter(school_id=school_id, paid_amount=data['paid_amount'], date_paid=data['date_paid'])
        if existing_payment.exists():
            raise serializers.ValidationError("A payment with the same amount and date already exists for this school.")
        return data

class PryPaymentSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(max_length=255, write_only=True)
    school = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PryPayments
        fields = ['id', 'school', 'school_name', 'paid_amount', 'date_paid' ]

    def validate_school_name(self, value):
        try:
            school = PSchool.objects.get(name__iexact=value)
            return school.id
        except PSchool.DoesNotExist:
            raise serializers.ValidationError("School does not exist.")

    def create(self, validated_data):
        current_year = datetime.now().year
        current_month = datetime.now().month
        if current_month in [1, 2, 3, 4]:
            current_term = 1
        elif current_month in [5, 6, 7, 8]:
            current_term = 2
        else:
            current_term = 3

        school_id = validated_data.pop('school_name')
        last_payment = PryPayments.objects.filter(school_id=school_id).order_by('-id').first()
        if last_payment:
            balance = last_payment.balance + validated_data['paid_amount']
        else:
            balance = validated_data['paid_amount']

        return PryPayments.objects.create(
            school_id=school_id,
            paid_amount=validated_data['paid_amount'],
            date_paid=validated_data['date_paid'],
            year=current_year,
            term=current_term,
            balance=balance
        )

    def validate(self, data):
        school_id = data.get('school_name')
        existing_payment = PryPayments.objects.filter(school_id=school_id, paid_amount=data['paid_amount'], date_paid=data['date_paid'])
        if existing_payment.exists():
            raise serializers.ValidationError("A payment with the same amount and date already exists for this school.")
        return data