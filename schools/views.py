# schools/views.py
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


from .models import (
    Admin, Users, PSchool, SSchool,
    PGradeEnrollment, SGradeEnrollment,
    PTeacherData, STeacherData,
    PryPayments, SecPayments, Messages
)
from .serializer import (
    MyTokenObtainPairSerializer,
    UserProfileSerializer, AdminProfileSerializer,
     AdminCreationSerializer,
    PSchoolSerializer, SSchoolSerializer,
    PGradeEnrollmentSerializer, SGradeEnrollmentSerializer,
    PTeacherDataSerializer, STeacherDataSerializer,
    ExcelUploadSerializer, CSVUploadSerializer,
    PryPaymentSerializer, SecPaymentSerializer,MessageSerializer,
    PryPaymentsListSerializer, SecPaymentsListSerializer, AdminUserUpdateSerializer, PublicMessageSerializer,
)
from .utils import (
    dataframe_to_excel_response,
    get_current_year_term
)

import pandas as pd
import logging

logger = logging.getLogger(__name__)

# =======================
# --- JWT Auth ---
# =======================
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MyTokenRefreshView(TokenRefreshView):
    pass

User = get_user_model()

# =======================
# --- User & Admin Management ---
# =======================
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

from rest_framework import generics, mixins





class UserListUpdateView(mixins.UpdateModelMixin,
                         generics.ListAPIView):
    """
    GET    /users/         → List all users
    PATCH  /users/<pk>/    → Partially update a user (e.g., promote to admin)
    """
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all().order_by("id")
    serializer_class = UserProfileSerializer  # default for GET

    def get_serializer_class(self):
        # Use update-capable serializer for PUT/PATCH
        if self.request.method in ["PUT", "PATCH"]:
            return AdminUserUpdateSerializer
        return UserProfileSerializer

    def patch(self, request, *args, **kwargs):
        """Handle partial updates (PATCH)."""
        return self.partial_update(request, *args, **kwargs)




class AdminProfileListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Admin.objects.all().order_by("phone_number")
    serializer_class = AdminProfileSerializer

class AdminUserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Admin.objects.all()
    serializer_class = AdminProfileSerializer

    def update(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response({"detail": "Forbidden"}, status=403)
        return super().update(request, *args, **kwargs)

class AdminUserCreationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AdminUserUpdateSerializer

class AdminCreationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AdminCreationSerializer

# =======================
# --- Excel Upload / Export ---
# =======================


class ExcelExportView(APIView):
    """Export schools data as Excel"""
    permission_classes = [IsAuthenticated]

    def get(self, request, model):
        model = model.lower()
        if model == "pschool":
            df = pd.DataFrame(PSchool.objects.all().values())
            return dataframe_to_excel_response(df, "PSchools.xlsx")
        elif model == "sschool":
            df = pd.DataFrame(SSchool.objects.all().values())
            return dataframe_to_excel_response(df, "SSchools.xlsx")
        return Response({"error": "Invalid model"}, status=400)

# =======================
# --- CSV Upload ---
# =======================
class CSVUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        ser = CSVUploadSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        df = pd.read_csv(ser.validated_data["csv_file"], skiprows=5, on_bad_lines="skip")
        year, term = get_current_year_term()
        created = 0
        for _, row in df.iterrows():
            # TODO: Implement CSV processing logic
            created += 1
        return Response({"records_created": created}, status=201)

# =======================
# --- Schools ---
# =======================
class PSchoolListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PSchool.objects.all()
    serializer_class = PSchoolSerializer

class SSchoolListView(PSchoolListView):
    queryset = SSchool.objects.all()
    serializer_class = SSchoolSerializer

# =======================
# --- Grade Enrollments ---
# =======================
class PGradeEnrollmentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PGradeEnrollment.objects.all()
    serializer_class = PGradeEnrollmentSerializer

class SGradeEnrollmentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SGradeEnrollment.objects.all()
    serializer_class = SGradeEnrollmentSerializer

# =======================
# --- Teacher Data ---
# =======================
class PTeacherDataListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PTeacherData.objects.all()
    serializer_class = PTeacherDataSerializer

class STeacherDataListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = STeacherData.objects.all()
    serializer_class = STeacherDataSerializer

# =======================
# --- Payments ---
# =======================


class PryPaymentViewSet(viewsets.ModelViewSet):
    queryset = PryPayments.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PryPaymentsListSerializer
        return PryPaymentSerializer


class SecPaymentViewSet(viewsets.ModelViewSet):
    queryset = SecPayments.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SecPaymentsListSerializer
        return SecPaymentSerializer


class PryPaymentDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PryPayments.objects.all()
    serializer_class = PryPaymentSerializer



class SecPaymentDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SecPayments.objects.all()
    serializer_class = SecPaymentSerializer



class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Users, pk=self.request.user.pk)

    def get_serializer_context(self):
        """ Ensure serializer has access to request so get_profile() can build absolute URLs for images. """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().patch(request, *args, **kwargs)
    



import datetime
import pandas as pd
import logging
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import (
    PSchool, SSchool,
    PGradeEnrollment, SGradeEnrollment
)
from .serializer import ExcelUploadSerializer

logger = logging.getLogger(__name__)

class PrimaryExcelUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = ExcelUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        excel_file = serializer.validated_data['file']
        try:
            df = pd.read_excel(excel_file, sheet_name='PRIMARY ENROL', skiprows=2)
            updated = 0
            created = 0
            current_year = datetime.datetime.now().year

            for _, row in df.iterrows():
                school_name = str(row[1]) if pd.notna(row[1]) else None
                district = str(row[0]) if pd.notna(row[0]) else None
                registration = str(row[2]) if pd.notna(row[2]) else None
                if not school_name or not district:
                    continue

                pschool_obj, created_school = PSchool.objects.get_or_create(
                    name=school_name,
                    district=district,
                    year=current_year,
                    defaults={'registration_status': registration}
                )

                if not created_school:
                    pschool_obj.registration_status = registration
                    pschool_obj.save()

                def safe(val):
                    try:
                        return int(float(val))
                    except (ValueError, TypeError):
                        return None

                grade_map = {
                    'ecd_a': (3, 4, 5),
                    'ecd_b': (6, 7, 8),
                    'grade_1': (9, 10, 11),
                    'grade_2': (12, 13, 14),
                    'grade_3': (15, 16, 17),
                    'grade_4': (18, 19, 20),
                    'grade_5': (21, 22, 23),
                    'grade_6': (24, 25, 26),
                    'grade_7': (27, 28, 29),
                    'grand_total': (30, 31, 32),
                }

                for grade, (m, f, t) in grade_map.items():
                    male = safe(row[m]) if m < len(row) else None
                    female = safe(row[f]) if f < len(row) else None
                    total = safe(row[t]) if t < len(row) else None

                    if male or female or total:
                        enrollment_obj, created_enrollment = PGradeEnrollment.objects.get_or_create(
                            school=pschool_obj,
                            level=grade,
                            year=current_year,
                            defaults={'male': male, 'female': female, 'total': total}
                        )
                        if not created_enrollment:
                            enrollment_obj.male = male
                            enrollment_obj.female = female
                            enrollment_obj.total = total
                            enrollment_obj.save()
                            updated += 1
                        else:
                            created += 1

            return Response(
                {"status": "success", "records_updated": updated, "records_created": created},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.exception("Primary Excel upload failed")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SecondaryExcelUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = ExcelUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        excel_file = serializer.validated_data['file']
        try:
            df = pd.read_excel(excel_file, sheet_name='SECONDARY ENROL', skiprows=2)
            updated = 0
            created = 0
            current_year = datetime.datetime.now().year

            for _, row in df.iterrows():
                school_name = str(row[1]) if pd.notna(row[1]) else None
                district = str(row[0]) if pd.notna(row[0]) else None
                registration = str(row[2]) if pd.notna(row[2]) else None
                if not school_name or not district:
                    continue

                sschool_obj, created_school = SSchool.objects.get_or_create(
                    name=school_name,
                    district=district,
                    year=current_year,
                    defaults={'registration_status': registration}
                )

                if not created_school:
                    sschool_obj.registration_status = registration
                    sschool_obj.save()

                def safe(val):
                    try:
                        return int(float(val))
                    except (ValueError, TypeError):
                        return None

                grade_map = {
                    'form_1': (3, 4, 5),
                    'form_2': (6, 7, 8),
                    'form_3': (9, 10, 11),
                    'form_4': (12, 13, 14),
                    'form_5': (15, 16, 17),
                    'form_6': (18, 19, 20),
                    'grand_total': (21, 22, 23),
                }

                for grade, (m, f, t) in grade_map.items():
                    male = safe(row[m]) if m < len(row) else None
                    female = safe(row[f]) if f < len(row) else None
                    total = safe(row[t]) if t < len(row) else None

                    if male or female or total:
                        enrollment_obj, created_enrollment = SGradeEnrollment.objects.get_or_create(
                            school=sschool_obj,
                            level=grade,
                            year=current_year,
                            defaults={'male': male, 'female': female, 'total': total}
                        )
                        if not created_enrollment:
                            enrollment_obj.male = male
                            enrollment_obj.female = female
                            enrollment_obj.total = total
                            enrollment_obj.save()
                            updated += 1
                        else:
                            created += 1

            return Response(
                {"status": "success", "records_updated": updated, "records_created": created},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.exception("Secondary Excel upload failed")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import datetime
import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)
ogger = logging.getLogger(__name__)

def get_current_term():
    current_month = datetime.datetime.now().month
    if current_month in [1, 2, 3, 4]:
        return 1
    elif current_month in [5, 6, 7, 8]:
        return 2
    else:
        return 3

def _update_balance_for_type(SchoolModel, GradeEnrollmentModel, PaymentsModel, multiplier):
    current_term = get_current_term()
    current_year = datetime.datetime.now().year
    logger.info(f"Updating {SchoolModel.__name__}: term {current_term}, year {current_year}")
    
    for school in SchoolModel.objects.all():
        try:
            grade_enrollment = GradeEnrollmentModel.objects.get(
                school=school, level='grand_total', year=current_year
            )
            grand_total = (grade_enrollment.total or 0) * multiplier
            
            # previous term's payments
            if current_term == 1:
                previous_payments = PaymentsModel.objects.filter(
                    school=school, year=current_year - 1
                ).order_by('-id')
            else:
                previous_payments = PaymentsModel.objects.filter(
                    school=school, year=current_year, term=current_term - 1
                ).order_by('-id')
            
            if previous_payments.exists():
                prev = previous_payments.first()
                balance = prev.balance - grand_total
                logger.info(f"Prev payment found for {school.id}, balance: {balance}")
            else:
                balance = -grand_total
                logger.info(f"No prev payment for {school.id}, balance: {balance}")
            
            # Create or get this term's payment record
            new_payment, created = PaymentsModel.objects.get_or_create(
                school=school, year=current_year, term=current_term,
                defaults={
                    'paid_amount': 0,
                    'date_paid': None,
                    'balance': balance,
                }
            )
            if created:
                logger.info(f"New payment created for {school.id}")
            else:
                logger.info(f"Payment already exists for {school.id}")
        except GradeEnrollmentModel.DoesNotExist:
            logger.error(f"No grade enrollment for {school.id}")

class UpdateBalanceView(APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        _update_balance_for_type(PSchool, PGradeEnrollment, PryPayments, multiplier=2)
        _update_balance_for_type(SSchool, SGradeEnrollment, SecPayments, multiplier=4)
        return Response({"status": "successfully records created"}, status=status.HTTP_201_CREATED)
        
# Create and list messages

# views.py

class PublicMessagesView(generics.ListAPIView):
    queryset = Messages.objects.all().order_by('-id')
    serializer_class = PublicMessageSerializer
    permission_classes =[AllowAny]


# views.py

class MessageListCreateDeleteView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Messages.objects.all().order_by('-id')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        dept = user.admin.department if user.admin else "Unknown"
        serializer.save(user=user, department=dept)

class EditMessageView(generics.RetrieveUpdateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

