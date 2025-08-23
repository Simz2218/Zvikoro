from rest_framework import status, generics
import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import(PSchoolSerializer, PGradeEnrollmentSerializer, 
    MyTokenObtainPairSerializer,
    AdminSerializer,
    AdminUserCreationSerializer,
    EmployeeRecordSerializer,
   PTeacherDataSerializer,
   STeacherDataSerializer,
   SecondaryExcelUploadSerializer,
   SSchoolSerializer, SGradeEnrollmentSerializer,PryPaymentSerializer, SecPaymentSerializer,PryPaymentsSerializer, SecPaymentsSerializer,CSVUploadSerializer,
    
    ExcelUploadSerializer
)
from .models import Admin,Users,  PSchool, PGradeEnrollment, PTeacherData,SSchool, SGradeEnrollment, STeacherData, PryPayments, SecPayments
import logging
import csv
from django.http import HttpResponse
from datetime import date
import datetime
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import NotFound
import csv

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = AdminUserCreationSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminView(generics.ListAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

class AdminUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Admin.objects.get(pk=pk)
        except Admin.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if user and (request.user.is_admin or int(pk) == request.user.pk):
            serializer = AdminSerializer(user) if pk == str(request.user.pk) else EmployeeRecordSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "User not found or you are not authorized."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        user = self.get_object(pk)
        if user and (request.user.is_admin or int(pk) == request.user.pk):
            serializer = AdminUserCreationSerializer(user, data=request.data, partial=True) if pk == str(request.user.pk) else EmployeeRecordSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "User not found or you are not authorized."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user and request.user.is_admin and int(pk) != request.user.pk:
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "User not found or you are not authorized."}, status=status.HTTP_404_NOT_FOUND)

class AdminUserCreationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AdminUserCreationSerializer
    def create(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip()  # Get email from request data

        # Check if email is provided and unique
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        if Users.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class EmployeeRecordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmployeeRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PrimaryExcelUploadView(APIView):
    def post(self, request, format=None):
        serializer = ExcelUploadSerializer(data=request.data)
        if serializer.is_valid():
            excel_file = serializer.validated_data['file']
            try:
                df = pd.read_excel(excel_file, sheet_name='PRIMARY ENROL', skiprows=2)
                updated = 0
                created = 0
                current_year = datetime.datetime.now().year
                for _, row in df.iterrows():
                    # Ensure the row is properly formatted
                    school_name = str(row[1]) if pd.notna(row[1]) else None
                    district = str(row[0]) if pd.notna(row[0]) else None
                    registration = str(row[2]) if pd.notna(row[2]) else None
                    if not school_name or not district:
                        continue

                    pschool_obj, created_school = PSchool.objects.get_or_create(
                        name=school_name,
                        district=district,
                        defaults={
                            'registration_status': registration,
                        }
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
                                defaults={
                                    'male': male,
                                    'female': female,
                                    'total': total,
                                }
                            )
                            if not created_enrollment:
                                enrollment_obj.male = male
                                enrollment_obj.female = female
                                enrollment_obj.total = total
                                enrollment_obj.save()
                                updated += 1
                            else:
                                created += 1
                return Response({'status': 'success', 'records_updated': updated, 'records_created': created}, status=201)
            except Exception as e:
                return Response({'error': str(e)}, status=500)
        return Response(serializer.errors, status=400)

class PSchoolListView(APIView):
    def get(self, request):
        PSchools = PSchool.objects.all()
        serializer = PSchoolSerializer(PSchools, many=True)
        return Response(serializer.data)

class PGradeEnrollmentListView(APIView):
    def get(self, request):
        grade_enrollments = PGradeEnrollment.objects.all()
        serializer = PGradeEnrollmentSerializer(grade_enrollments, many=True)
        return Response(serializer.data)

class PTeacherDataListView(APIView):
    def get(self, request):
        teacher_data = PTeacherData.objects.all()
        serializer = PTeacherDataSerializer(teacher_data, many=True)
        return Response(serializer.data)

class PSchoolDetailView(APIView):
    def get(self, request, pk):
        try:
            PSchool = PSchool.objects.get(pk=pk)
            serializer = PSchoolSerializer(PSchool)
            return Response(serializer.data)
        except PSchool.DoesNotExist:
            return Response({'error': 'PSchool not found'}, status=404)

    def put(self, request, pk):
        try:
            PSchool = PSchool.objects.get(pk=pk)
            serializer = PSchoolSerializer(PSchool, data=request.data)
            if serializer.is_valid():
                if 'year' not in request.data:
                    request.data['year'] = PSchool.year
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except PSchool.DoesNotExist:
            return Response({'error': 'PSchool not found'}, status=404)

class PGradeEnrollmentDetailView(APIView):
    def get(self, request, pk):
        try:
            grade_enrollment = PGradeEnrollment.objects.get(pk=pk)
            serializer = PGradeEnrollmentSerializer(grade_enrollment)
            return Response(serializer.data)
        except PGradeEnrollment.DoesNotExist:
            return Response({'error': 'Grade Enrollment not found'}, status=404)

    def put(self, request, pk):
        try:
            grade_enrollment = PGradeEnrollment.objects.get(pk=pk)
            serializer = PGradeEnrollmentSerializer(grade_enrollment, data=request.data)
            if serializer.is_valid():
                if 'year' not in request.data:
                    request.data['year'] = grade_enrollment.year
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except PGradeEnrollment.DoesNotExist:
            return Response({'error': 'Grade Enrollment not found'}, status=404)

class PTeacherDataDetailView(APIView):
    def get(self, request, pk):
        try:
            teacher_data = PTeacherData.objects.get(pk=pk)
            serializer = PTeacherDataSerializer(teacher_data)
            return Response(serializer.data)
        except PTeacherData.DoesNotExist:
            return Response({'error': 'Teacher Data not found'}, status=404)

    def put(self, request, pk):
        try:
            teacher_data = PTeacherData.objects.get(pk=pk)
            serializer = PTeacherDataSerializer(teacher_data, data=request.data)
            if serializer.is_valid():
                if 'year' not in request.data:
                    request.data['year'] = teacher_data.year
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except PTeacherData.DoesNotExist:
            return Response({'error': 'Teacher Data not found'}, status=404)

class PrimaryExcelExportView(APIView):
    def get(self, request, model):
        model = model.lower()
        if model == 'pschool':
            data = PSchool.objects.all().values()
            df = pd.DataFrame(list(data))
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="PSchools.xlsx"'
            df.to_excel(response, index=False)
            return response
        elif model == 'pgradeenrollment':
            data = PGradeEnrollment.objects.all().values()
            df = pd.DataFrame(list(data))
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="grade_enrollments.xlsx"'
            df.to_excel(response, index=False)
            return response
        elif model == 'pteacherData':
            data = PTeacherData.objects.all().values()
            df = pd.DataFrame(list(data))
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="teacher_data.xlsx"'
            df.to_excel(response, index=False)
            return response
        return Response({'error': 'Invalid model'}, status=400)
    
    
    
    # secondary schools views 
    
class SecondaryExcelUploadView(APIView):
    def post(self, request, format=None):
        serializer = SecondaryExcelUploadSerializer(data=request.data)
        if serializer.is_valid():
            excel_file = serializer.validated_data['file']
            try:
                df = pd.read_excel(excel_file, sheet_name='SECONDARY ENROL', skiprows=2)
                updated = 0
                created = 0
                current_year = datetime.datetime.now().year
                for _, row in df.iterrows():
                    # Ensure the row is properly formatted
                    school_name = str(row[1]) if pd.notna(row[1]) else None
                    district = str(row[0]) if pd.notna(row[0]) else None
                    registration = str(row[2]) if pd.notna(row[2]) else None
                    if not school_name or not district:
                        continue

                    school_obj, created_school = SSchool.objects.get_or_create(
                        name=school_name,
                        district=district,
                        defaults={
                            'registration_status': registration,
                        },
                        year=current_year
                    )
                    if not created_school:
                        school_obj.registration_status = registration
                        school_obj.save()

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
                                school=school_obj,
                                level=grade,
                                year=current_year,
                                defaults={
                                    'male': male,
                                    'female': female,
                                    'total': total,
                                }
                            )
                            if not created_enrollment:
                                enrollment_obj.male = male
                                enrollment_obj.female = female
                                enrollment_obj.total = total
                                enrollment_obj.save()
                                updated += 1
                            else:
                                created += 1
                return Response({'status': 'success', 'records_updated': updated, 'records_created': created}, status=201)
            except Exception as e:
                return Response({'error': str(e)}, status=500)
        return Response(serializer.errors, status=400)

    
class SSchoolListView(APIView):
    def get(self, request):
        SSchools = SSchool.objects.all()
        serializer = SSchoolSerializer(SSchools, many=True)
        return Response(serializer.data)

class SGradeEnrollmentListView(APIView):
    def get(self, request):
        grade_enrollments = SGradeEnrollment.objects.all()
        serializer = SGradeEnrollmentSerializer(grade_enrollments, many=True)
        return Response(serializer.data)

class STeacherDataListView(APIView):
    def get(self, request):
        teacher_data = STeacherData.objects.all()
        serializer = STeacherDataSerializer(teacher_data, many=True)
        return Response(serializer.data)

class SSchoolDetailView(APIView):
    def get(self, request, pk):
        try:
            SSchool = SSchool.objects.get(pk=pk)
            serializer = SSchoolSerializer(SSchool)
            return Response(serializer.data)
        except SSchool.DoesNotExist:
            return Response({'error': 'SSchool not found'}, status=404)

    def put(self, request, pk):
        try:
            SSchool = SSchool.objects.get(pk=pk)
            serializer = SSchoolSerializer(SSchool, data=request.data)
            if serializer.is_valid():
                if 'year' not in request.data:
                    request.data['year'] = SSchool.year
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except SSchool.DoesNotExist:
            return Response({'error': 'SSchool not found'}, status=404)

class SGradeEnrollmentDetailView(APIView):
    def get(self, request, pk):
        try:
            grade_enrollment = SGradeEnrollment.objects.get(pk=pk)
            serializer = SGradeEnrollmentSerializer(grade_enrollment)
            return Response(serializer.data)
        except SGradeEnrollment.DoesNotExist:
            return Response({'error': 'Grade Enrollment not found'}, status=404)

    def put(self, request, pk):
        try:
            grade_enrollment = SGradeEnrollment.objects.get(pk=pk)
            serializer = SGradeEnrollmentSerializer(grade_enrollment, data=request.data)
            if serializer.is_valid():
                if 'year' not in request.data:
                    request.data['year'] = grade_enrollment.year
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except SGradeEnrollment.DoesNotExist:
            return Response({'error': 'Grade Enrollment not found'}, status=404)

class STeacherDataDetailView(APIView):
    def get(self, request, pk):
        try:
            teacher_data = STeacherData.objects.get(pk=pk)
            serializer = STeacherDataSerializer(teacher_data)
            return Response(serializer.data)
        except STeacherData.DoesNotExist:
            return Response({'error': 'Teacher Data not found'}, status=404)

    def put(self, request, pk):
        try:
            teacher_data = STeacherData.objects.get(pk=pk)
            serializer = STeacherDataSerializer(teacher_data, data=request.data)
            if serializer.is_valid():
                if 'year' not in request.data:
                    request.data['year'] = teacher_data.year
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except STeacherData.DoesNotExist:
            return Response({'error': 'Teacher Data not found'}, status=404)

class SecondaryExcelExportView(APIView):
    def get(self, request, model):
        model = model.lower()
        if model == 'sschool':
            data = SSchool.objects.all().values()
            df = pd.DataFrame(list(data))
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="SSchools.xlsx"'
            df.to_excel(response, index=False)
            return response
        elif model == 'sgradeenrollment':
            data = SGradeEnrollment.objects.all().values()
            df = pd.DataFrame(list(data))
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="grade_enrollments.xlsx"'
            df.to_excel(response, index=False)
            return response
        elif model == 'steacherData':
            data = STeacherData.objects.all().values()
            df = pd.DataFrame(list(data))
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="teacher_data.xlsx"'
            df.to_excel(response, index=False)
            return response
        return Response({'error': 'Invalid model'}, status=400)
    
    
    

import pandas as pd

import datetime

import logging
logger = logging.getLogger(__name__)

class UploadCSVView(APIView):
    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.validated_data['csv_file']
            try:
                df = pd.read_csv(csv_file, skiprows=5, on_bad_lines='skip')
                created = 0
                current_year = datetime.date.today().year
                current_term = self.get_current_term()
                for index, row in df.iterrows():
                    try:
                        if len(row) >= 7:
                            date_paid_str = str(row.iloc[0])
                            date_paid = self.parse_date_paid(date_paid_str)
                            narration = str(row.iloc[3])
                            paid_amount = float(row.iloc[5]) if pd.notnull(row.iloc[5]) else float(row.iloc[4]) if pd.notnull(row.iloc[4]) else 0
                            school = self.get_school(narration)
                            if school:
                                logger.info(f"Processing row {index}: school={school.name}, paid_amount={paid_amount}, date_paid={date_paid}")
                                self.create_payment(school, paid_amount, date_paid, current_year, current_term)
                                created += 1
                                logger.info(f"Payment created for row {index}")
                            else:
                                logger.warning(f"School not found for row {index}: narration={narration}")
                    except Exception as e:
                        logger.error(f"Error processing row {index}: {str(e)}")
                return Response({'message': 'CSV file uploaded successfully', 'records_created': created}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error processing CSV file: {str(e)}")
                return Response({'error': 'Error processing CSV file'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_current_term(self):
        current_month = datetime.date.today().month
        if current_month in [1, 2, 3, 4]:
            return 1
        elif current_month in [5, 6, 7, 8]:
            return 2
        else:
            return 3

    def get_school(self, narration):
        school_name = narration.split()[-1].strip().lower()
        school_name = ''.join(e for e in school_name if e.isalnum())
        school_models = {
            'pry': PSchool,
            'primary': PSchool,
            'sec': SSchool,
            'secondary': SSchool,
            'high': SSchool,
        }
        for keyword, school_model in school_models.items():
            if keyword in school_name:
                school_name_without_keyword = school_name.replace(keyword, '').strip()
                return school_model.objects.filter(name__icontains=school_name_without_keyword).first()
        return PSchool.objects.filter(name__icontains=school_name).first() or SSchool.objects.filter(name__icontains=school_name).first()
    def parse_date_paid(self, date_paid_str):
        date_paid = datetime.datetime.strptime(date_paid_str[:10], '%Y-%m-%d')
        return int(date_paid.strftime('%Y%m%d'))

    def create_payment(self, school, paid_amount, date_paid, year, term):
        if isinstance(school, PSchool):
            payment_model = PryPayments
        elif isinstance(school, SSchool):
            payment_model = SecPayments
        else:
            return
        last_payment = payment_model.objects.filter(school=school).order_by('-id').first()
        if last_payment:
            balance = last_payment.balance - paid_amount
        else:
            balance = -paid_amount
        payment_model.objects.create(
            school=school,
            paid_amount=paid_amount,
            date_paid=date_paid,
            balance=balance,
            year=year,
            term=term
        )
class PryPaymentUpdateView(UpdateAPIView):
    queryset = PryPayments.objects.all()
    serializer_class = PryPaymentSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            update_balance(instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SecPaymentUpdateView(UpdateAPIView):
    queryset = SecPayments.objects.all()
    serializer_class = SecPaymentSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            update_balance(instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PryPaymentView(APIView):
    def get(self, request):
        payments = PryPayments.objects.all()
        serializer = PryPaymentsSerializer(payments, many=True)
        return Response(serializer.data)

class SecPaymentView(APIView):
    def get(self, request):
        payments = SecPayments.objects.all()
        serializer = SecPaymentsSerializer(payments, many=True)
        return Response(serializer.data)
    
class CreateSecPaymentView(APIView):
    def post(self, request):
        serializer = SecPaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreatePryPaymentView(APIView):
    def post(self, request):
        serializer = PryPaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_balance(request):
    current_month = datetime.datetime.now().month
    if current_month in [1, 2, 3, 4]:
        current_term = 1
    elif current_month in [5, 6, 7, 8]:
        current_term = 2
    else:
        current_term = 3

    current_year = datetime.datetime.now().year
    logger.info(f"Current term: {current_term}, Current year: {current_year}")

    # Update balance for PSchool
    pschools = PSchool.objects.all()
    for school in pschools:
        try:
            grade_enrollment = PGradeEnrollment.objects.get(school=school, level='grand_total', year=current_year)
            if grade_enrollment.total is not None:
                grand_total = grade_enrollment.total * 2
            else:
                grand_total = 0

            # Get previous term's payment
            if current_term == 1:
                previous_payments = PryPayments.objects.filter(school=school, year=current_year - 1).order_by('-id')
            else:
                previous_payments = PryPayments.objects.filter(school=school, year=current_year, term=current_term - 1).order_by('-id')

            if previous_payments.exists():
                previous_payment = previous_payments[0]
                balance = previous_payment.balance - grand_total
                logger.info(f"Previous payment found for school {school.id}. Balance: {balance}")
            else:
                balance = -grand_total
                logger.info(f"No previous payment found for school {school.id}. Balance: {balance}")

            # Create new payment instance
            new_payment, created = PryPayments.objects.get_or_create(
                school=school,
                year=current_year,
                term=current_term,
                defaults={
                    'paid_amount': 0,
                    'date_paid': None,
                    'balance': balance
                }
            )
            if created:
                logger.info(f"New payment created for school {school.id}.")
            else:
                logger.info(f"Payment already exists for school {school.id}.")

        except PGradeEnrollment.DoesNotExist:
            logger.error(f"No grade enrollment found for school {school.id}.")

    # Update balance for SSchool
    sschools = SSchool.objects.all()
    for school in sschools:
        try:
            grade_enrollment = SGradeEnrollment.objects.get(school=school, level='grand_total', year=current_year)
            if grade_enrollment.total is not None:
                grand_total = grade_enrollment.total * 4
            else:
                grand_total = 0

            # Get previous term's payment
            if current_term == 1:
                previous_payments = SecPayments.objects.filter(school=school, year=current_year - 1).order_by('-id')
            else:
                previous_payments = SecPayments.objects.filter(school=school, year=current_year, term=current_term - 1).order_by('-id')

            if previous_payments.exists():
                previous_payment = previous_payments[0]
                balance = previous_payment.balance - grand_total
                logger.info(f"Previous payment found for school {school.id}. Balance: {balance}")
            else:
                balance = -grand_total
                logger.info(f"No previous payment found for school {school.id}. Balance: {balance}")

            # Create new payment instance
            new_payment, created = SecPayments.objects.get_or_create(
                school=school,
                year=current_year,
                term=current_term,
                defaults={
                    'paid_amount': 0,
                    'date_paid': None,
                    'balance': balance
                }
            )
            if created:
                logger.info(f"New payment created for school {school.id}.")
            else:
                logger.info(f"Payment already exists for school {school.id}.")

        except SGradeEnrollment.DoesNotExist:
            logger.error(f"No grade enrollment found for school {school.id}.")

    return HttpResponse("Balance updated successfully")