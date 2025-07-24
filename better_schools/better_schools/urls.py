from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from schools.views import (
    UserProfileUpdateView,
    AdminUserDetailView,
    AdminUserCreationView,
    EmployeeRecordView,
    SchoolUpdateView,
    AdminSchoolUpdateView,
    MyTokenObtainPairView,
    AdminView,
)

urlpatterns = [
    # User profile update view
    path('profile/update/', UserProfileUpdateView.as_view()),

    # Admin user detail view
    path('users/<int:pk>/', AdminUserDetailView.as_view()),
    
    # Token user login
    path('token/', MyTokenObtainPairView.as_view()),
    
    # Token Refresh
    path('token/refresh/', TokenRefreshView.as_view()),

    # Admin user creation view
    path('users/<str:phone_number>/', AdminUserCreationView.as_view(),name='update_admin'),

    # Employee record view
    path('employees/create/', EmployeeRecordView.as_view()),

    # School update view
    path('school/update/', SchoolUpdateView.as_view()),

    # Admin school update view
    path('schools/<int:pk>/update/', AdminSchoolUpdateView.as_view()),
   
   # Admin school update view
    path('admin/list/', AdminView.as_view()), 
    
]
