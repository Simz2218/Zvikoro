from schools.models import Admin, Schools, Payment, Balances, Users

from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers 
from django.core.exceptions import ObjectDoesNotExist


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Users
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):

        token = super().get_token(user)
        
        token['surname']= Admin.surname
        token['first_name']= Admin.first_name
        token['profile']= Users.profile 
        token['username']= Users.username
        token['department']= Admin.department
        token['phone_number']= Admin.phone_number
        token['is_admin']= Users.is_admin
        
        return token 

class AdminUserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ['phone_number', 'username', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields don't match."})
        if Admin.objects.filter(username=attrs['username']).exclude(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({"username": "User with this username already exists."})
        return attrs
    def validate_phone_number(self, value):
        try:
            admin = Admin.objects.get(phone_number=value)
            if Users.username and Users.password:
                raise serializers.ValidationError("User with this phone number already exists and has a username and password.")
        except Admin.DoesNotExist:
            raise serializers.ValidationError("Admin with this phone number does not exist")
        return value

    def create(self, instance, validated_data):
        instance.phone_number=validated_data
        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

    
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




class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schools
        fields = ['id', 'name', 'enrolment', 'phone_number']

class SchoolUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Schools
        fields = ['enrolment', 'phone_number']

    

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


####
class AdminSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schools
        fields = '_all_'

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    ## payment serializers 
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'payment_date', 'payment_method', 'status', 'receipt_collected', 'receipt_created']

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['user', 'amount', 'payment_method']

class PaymentBulkUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balances
        fields = ['id', 'school', 'balance', 'term', 'year', 'enrolment']
