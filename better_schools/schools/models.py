from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
import uuid
from encrypted_model_fields.fields import EncryptedCharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime



 


class Admin(models.Model):
    phone_number = models.CharField(max_length=10, unique=True,primary_key=True,  editable=True)
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    
     # Ensure Pillow is installed
    department = models.CharField(max_length=30)
    password = EncryptedCharField(max_length=200)  # Encrypted password
 # Admins are true by default
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    REQUIRED_FIELDS = ['name', 'surname',  'department']  # Add required fields

    def __str__(self):
        return f"{self.name} {self.surname}"

    # Unique related names to avoid clashes
    

class Users(AbstractBaseUser, PermissionsMixin):
        username = models.CharField(max_length=100)
        email = models.EmailField(unique=True)
        password=models.CharField(max_length=21)
        phone_number = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='user')
        is_admin = models.BooleanField(default=False)
        profile = models.ImageField(default="default.jpg", upload_to="user_images")
        
        bio = models.CharField(max_length=1000)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['username']
        
        groups = models.ManyToManyField(Group, related_name='admin_set', blank=True)
        user_permissions = models.ManyToManyField(Permission, related_name='admin_set', blank=True)

class Schools(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    head = models.CharField(max_length=200)
    enrolment = models.CharField(max_length=200)
    school_level = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15, unique=True)  # Unique phone number
   
    
   

   
    REQUIRED_FIELDS = ['name', 'head', 'enrolment', 'school_level']  # Add required fields

    def __str__(self):
        return self.name

    # Unique related names to avoid clashes
    groups = models.ManyToManyField(Group, related_name='schools_set', blank=True)
    

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Schools, on_delete=models.CASCADE, related_name='payments')  # Link to Schools
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of the payment
    payment_date = models.DateTimeField(auto_now_add=True)  # Date of payment
    payment_method = models.CharField(max_length=50)  # e.g., Credit Card, Bank Transfer
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')  # Status of the payment
    receipt_collected = models.BooleanField(default=False)  # Indicates if receipt has been collected
    receipt_created = models.BooleanField(default=False)  # Indicates if receipt has been created

    def __str__(self):
        return (f"Payment of {self.amount} by {self.user.name} on "
                f"{self.payment_date.strftime('%Y-%m-%d')} - "
                f"Receipt Created: {'Yes' if self.receipt_created else 'No'}, "
                f"Receipt Collected: {'Yes' if self.receipt_collected else 'No'}")

class Balances(models.Model):
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, related_name='balances')
    updated_at = models.DateTimeField(auto_now=True)
    balance= models.IntegerField(default=0)
    term= models.IntegerField(default=1)
    year= models.IntegerField(default=0)
    enrolment = models.CharField(max_length=200)
    
    def create_balance_record(sender, instance, created, **kwargs):
        if created:
            current_term = get_current_term()
            current_year = get_current_year()
        Balances.objects.create(school=instance, term=current_term, year=current_year, enrolment=instance.enrolment, balance=0)

def get_current_term():
    # logic to determine current term based on date or other factors
    # for simplicity, let's assume term 1, 2, or 3
    current_month = datetime.now().month
    if current_month < 4:
        return 1
    elif current_month < 8:
        return 2
    else:
        return 3
def get_current_year():
    year= datetime.now().year()
     
    return year
