from django.contrib import admin
from schools.models import Users, Admin, BaseSchool,BasePaymentMixin

admin.site.register(Users,Admin,BaseSchool,BasePaymentMixin)