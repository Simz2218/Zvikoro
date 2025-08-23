from django.urls import path
from .views import (
    MyTokenObtainPairView,
    UserProfileUpdateView,
    AdminView,
    AdminUserDetailView,
    AdminUserCreationView,
    CreatePryPaymentView,
    CreateSecPaymentView,
    EmployeeRecordView,
    PrimaryExcelUploadView, PSchoolListView, PSchoolDetailView,
    PGradeEnrollmentListView, PGradeEnrollmentDetailView,
    PTeacherDataListView, PTeacherDataDetailView,
    PrimaryExcelExportView, 
    SecondaryExcelUploadView, SSchoolListView, SSchoolDetailView,
    SGradeEnrollmentListView, SGradeEnrollmentDetailView,
    STeacherDataListView, STeacherDataDetailView,
    SecondaryExcelExportView, UploadCSVView, PryPaymentView, SecPaymentView, PryPaymentUpdateView, SecPaymentUpdateView 
   
)
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from schools import views

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view()),
    path('user/profile/update/', UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('admins/', AdminView.as_view(), name='admin_list'),
    path('admins/<int:pk>/', AdminUserDetailView.as_view(), name='admin_detail'),
    path('admins/create/', AdminUserCreationView.as_view(), name='admin_create'),
    path('employees/', EmployeeRecordView.as_view(), name='employee_create'),
    path('upload-excel/', PrimaryExcelUploadView.as_view(), name='upload-excel'),
    path('PSchools/', PSchoolListView.as_view()),
    path('PSchools/<int:pk>/', PSchoolDetailView.as_view()),
    path('grade-enrollments/', PGradeEnrollmentListView.as_view()),
    path('grade-enrollments/<int:pk>/', PGradeEnrollmentDetailView.as_view()),
    path('teacher/teacher-data/', PTeacherDataListView.as_view()),
    path('teacher/teacher-data/<int:pk>/', PTeacherDataDetailView.as_view()),
    path('export/<str:model>/', PrimaryExcelExportView.as_view()),
     path('supload-excel/', SecondaryExcelUploadView.as_view(), name='upload-excel'),
    path('SSchools/', SSchoolListView.as_view()),
    path('SSchools/<int:pk>/', SSchoolDetailView.as_view()),
    path('sgrade-enrollments/', SGradeEnrollmentListView.as_view()),
    path('sgrade-enrollments/<int:pk>/', SGradeEnrollmentDetailView.as_view()),
    path('steacher/teacher-data/', STeacherDataListView.as_view()),
    path('steacher/teacher-data/<int:pk>/', STeacherDataDetailView.as_view()),
    path('sexport/<str:model>/', SecondaryExcelExportView.as_view()),
    path('upload-csv/', UploadCSVView.as_view(), name='upload_'),
    path('pry-payments/', PryPaymentView.as_view(), name='pry_payments'),
     path('updatebalances/', views.update_balance, name='Balances Update'),
    path('sec-payments/', SecPaymentView.as_view(), name='sec_payments'),
    path('prypayments/', CreatePryPaymentView.as_view(), name='pry_payments'),
    path('secpayments/', CreateSecPaymentView.as_view(), name='sec_payments'),
    path('pry-payments/<int:pk>/', PryPaymentUpdateView.as_view(), name='pry_payment_update'),
    path('sec-payments/<int:pk>/', SecPaymentUpdateView.as_view(), name='sec_payment_update'),
]