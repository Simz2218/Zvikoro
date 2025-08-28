from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    # Auth
    MyTokenObtainPairView, MyTokenRefreshView,

    # Users & Admins
    UserProfileUpdateView, UserDetailView,
    AdminProfileListView, AdminUserDetailView,
    AdminUserCreationView, AdminCreationView,

    # Upload / Export
    PrimaryExcelUploadView, ExcelExportView, CSVUploadView,
    SecondaryExcelUploadView,  # NEW – secondary Excel upload

    # Schools
    PSchoolListView, SSchoolListView,

    # Enrollments
    PGradeEnrollmentListView, SGradeEnrollmentListView,  # NEW

    # Teacher Data
    PTeacherDataListView, STeacherDataListView,          # NEW

    # Payments
    PryPaymentViewSet, PryPaymentDetailView,
    SecPaymentViewSet, SecPaymentDetailView,
    UserListUpdateView,
    MessageListCreateDeleteView,PublicMessagesView, MessageListCreateDeleteView, EditMessageView
)
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'pry-payments', PryPaymentViewSet, basename='pry-payments')
router.register(r'sec-payments', SecPaymentViewSet, basename='sec-payments')

urlpatterns = [
    # JWT
    
    path("token/",          MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/",  MyTokenRefreshView.as_view(),    name="token_refresh"),

    # Users
    path("users/", UserListUpdateView.as_view()),            # list
    path("users/<int:pk>/", UserListUpdateView.as_view()),   # update
    path("users/me/",       UserProfileUpdateView.as_view(), name="user-update"),
  
    path("register/",   AdminUserCreationView.as_view(), name="user-create"),  # linked to existing admin

    # Admins
    path("admins/",         AdminProfileListView.as_view(),  name="admin-list"),
    path("admins/create/",  AdminCreationView.as_view(),     name="admin-create"),  # create admin only
    path("admins/<str:pk>/",AdminUserDetailView.as_view(),   name="admin-detail"),

    # Upload / Export
    path("upload-excel/",   PrimaryExcelUploadView.as_view(),       name="upload-excel"),
    path("supload-excel/",  SecondaryExcelUploadView.as_view(),      name="supload-excel"),  # NEW
    path("export-excel/<str:model>/", ExcelExportView.as_view(), name="export-excel"),
    path("upload-csv/",     CSVUploadView.as_view(),         name="upload-csv"),

    # Schools
    path("primary-schools/",   PSchoolListView.as_view(),    name="primary-schools"),
    path("secondary-schools/", SSchoolListView.as_view(),    name="secondary-schools"),

    # Grade Enrollments (Primary + Secondary)
    path("grade-enrollments/",  PGradeEnrollmentListView.as_view(), name="grade-enrollments"),   # NEW
    path("sgrade-enrollments/", SGradeEnrollmentListView.as_view(), name="sgrade-enrollments"),  # NEW

    # Teacher Data (Primary + Secondary)
    path("teacher/teacher-data/",  PTeacherDataListView.as_view(), name="teacher-data"),         # NEW
    path("steacher/teacher-data/", STeacherDataListView.as_view(), name="steacher-data"),        # NEW

    
    path('update-balance/', views.UpdateBalanceView.as_view()),
    path('', include(router.urls)),
    ## messages: 
    # urls.py
    path('messages/public/', PublicMessagesView.as_view(), name='public-messages'),
    path('messages/', MessageListCreateDeleteView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/delete/', MessageListCreateDeleteView.as_view(), name='message-delete'),
    path('messages/<int:pk>/edit/', EditMessageView.as_view(), name='edit-message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
