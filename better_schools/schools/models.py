from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission, PermissionsMixin, BaseUserManager
import uuid
from django.utils import timezone
from encrypted_model_fields.fields import EncryptedCharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


class Admin(models.Model):
    
    phone_number = models.CharField(max_length=10, unique=True, primary_key=True)

    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    department = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.surname}"

    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Use set_password to hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(username, email, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
      # Phone number as CharField
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, related_name='users', null=True, blank=True)  # Link to Admin
    is_admin = models.BooleanField(default=False)
    profile = models.ImageField(default="default.jpg", upload_to="user_images")
    bio = models.CharField(max_length=1000, blank=True)  # Allow blank bio
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']  # Ensure email and phone_number are required fields

    objects = CustomUserManager()  # Set the custom manager

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_by_natural_key(self, username):
        return self.get(username=username)




class PSchool(models.Model):
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    registration_status = models.CharField(max_length=255)
    year = models.IntegerField()
    

    
class PGradeEnrollment(models.Model):
    school = models.ForeignKey(PSchool, on_delete=models.CASCADE)
    level = models.CharField(max_length=255)
    male = models.IntegerField(null=True, blank=True)
    female = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)    
    year = models.IntegerField()
    

class PTeacherData(models.Model):
    school = models.ForeignKey(PSchool, on_delete=models.CASCADE)
    level = models.CharField(max_length=50)
    male = models.PositiveIntegerField(null=True, blank=True)
    female = models.PositiveIntegerField(null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    authorized_establishment = models.PositiveIntegerField(null=True, blank=True)
    vacancies = models.PositiveIntegerField(null=True, blank=True)
    year = models.IntegerField()
    
class SSchool(models.Model):
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    registration_status = models.CharField(max_length=255)
    year = models.IntegerField()
    

    
class SGradeEnrollment(models.Model):
    school = models.ForeignKey(SSchool, on_delete=models.CASCADE)
    level = models.CharField(max_length=255)
    male = models.IntegerField(null=True, blank=True)
    female = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)    
    year = models.IntegerField()
    

class STeacherData(models.Model):
    school = models.ForeignKey(SSchool, on_delete=models.CASCADE)
    level = models.CharField(max_length=50)
    male = models.PositiveIntegerField(null=True, blank=True)
    female = models.PositiveIntegerField(null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    authorized_establishment = models.PositiveIntegerField(null=True, blank=True)
    vacancies = models.PositiveIntegerField(null=True, blank=True)
    year = models.IntegerField()


class PryPayments(models.Model):
    school=models.ForeignKey(PSchool, on_delete=models.CASCADE)
    paid_amount=models.IntegerField()
    date_paid=models.IntegerField(null=True)
    balance=models.IntegerField()
    receipt=models.IntegerField(null=True)
    
    year=models.IntegerField()
    term=models.IntegerField()
    
    

class SecPayments(models.Model):
    school=models.ForeignKey(SSchool, on_delete=models.CASCADE)
    paid_amount=models.IntegerField()
    receipt=models.IntegerField(null=True)
    date_paid=models.IntegerField(null=True)
    balance=models.IntegerField()
    year=models.IntegerField()
    term=models.IntegerField()    
   