from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

# -------------------------
# Admin & Users
# -------------------------
DEPARTMENT_CHOICES = [
    ("IT", "IT"),
    ("Accounts", "Accounts"),
    ("Administration", "Administration"),
    ("DSI", "DSI"),
    ("Inspectors", "Inspectors"),
    ("Remedial", "Remedial"),
    ("NonFormal", "NonFormal"),
    ("OfficeOrderly", "OfficeOrderly"),
    ("HR", "HR"),
    ("Aid", "Aid"),
]
class Admin(models.Model):
    phone_number = models.CharField(max_length=10, primary_key=True, unique=True)
    first_name   = models.CharField(max_length=255)
    surname      = models.CharField(max_length=255)
    department   = models.CharField(max_length=30, choices=DEPARTMENT_CHOICES, default="IT")
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.surname}"


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **xtra):
        if not username or not email:
            raise ValueError("Username and email required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **xtra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **xtra):
        xtra.setdefault("is_admin", True)
        return self.create_user(username, email, password, **xtra)





class Users(AbstractBaseUser, PermissionsMixin):
    username   = models.CharField(max_length=100, unique=True)
    email      = models.EmailField(unique=True)
    admin      = models.ForeignKey(Admin, null=True, blank=False,
                                   on_delete=models.SET_NULL,
                                   related_name="users")
    is_admin   = models.BooleanField(default=True)
    profile = models.ImageField(upload_to="user_images", default="default.jpg", null=True, blank=True)

    bio        = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD  = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()
    def get_profile_url(self, request=None):
        if self.profile and hasattr(self.profile, 'url'):
            if request:
                return request.build_absolute_uri(self.profile.url)
            return self.profile.url
        return None


# -------------------------
# Schools
# -------------------------

class BaseSchool(models.Model):
    name                = models.CharField(max_length=255)
    district            = models.CharField(max_length=255)
    registration_status = models.CharField(max_length=255)
    year                = models.IntegerField()

    class Meta:
        abstract = True

class PSchool(BaseSchool):
    pass

class SSchool(BaseSchool):
    pass

# -------------------------
# Data mixins (no DB table)
# -------------------------

class GradeEnrollmentMixin(models.Model):
    level  = models.CharField(max_length=50)
    male   = models.IntegerField(null=True, blank=True)
    female = models.IntegerField(null=True, blank=True)
    total  = models.IntegerField(null=True, blank=True)
    year   = models.IntegerField()

    class Meta:
        abstract = True

class TeacherDataMixin(models.Model):
    level  = models.CharField(max_length=50)
    male   = models.PositiveIntegerField(null=True, blank=True)
    female = models.PositiveIntegerField(null=True, blank=True)
    total  = models.PositiveIntegerField(null=True, blank=True)
    authorized_establishment = models.PositiveIntegerField(null=True, blank=True)
    vacancies = models.PositiveIntegerField(null=True, blank=True)
    year      = models.IntegerField()

    class Meta:
        abstract = True

class BasePaymentMixin(models.Model):
    paid_amount = models.IntegerField()
    date_paid   = models.IntegerField(null=True, blank=True)
    balance     = models.IntegerField()
    receipt     = models.IntegerField(null=True, blank=True)
    year        = models.IntegerField()
    term        = models.IntegerField()

    class Meta:
        abstract = True

# -------------------------
# Concrete related models
# -------------------------

class PGradeEnrollment(GradeEnrollmentMixin):
    school = models.ForeignKey(PSchool, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Primary grade enrollments"

class SGradeEnrollment(GradeEnrollmentMixin):
    school = models.ForeignKey(SSchool, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Secondary grade enrollments"

class PTeacherData(TeacherDataMixin):
    school = models.ForeignKey(PSchool, on_delete=models.CASCADE)

class STeacherData(TeacherDataMixin):
    school = models.ForeignKey(SSchool, on_delete=models.CASCADE)

class PryPayments(BasePaymentMixin):
    school = models.ForeignKey(PSchool, on_delete=models.CASCADE)

class SecPayments(BasePaymentMixin):
    school = models.ForeignKey(SSchool, on_delete=models.CASCADE)

# -------------------------
# Messages
# -------------------------

class Messages(models.Model):
    user       = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    message    = models.CharField(max_length=100)
    department = models.CharField(max_length=1000)
    
