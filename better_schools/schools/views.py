
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import MyTokenObtainPairSerializer,AdminSerializer, AdminUserCreationSerializer, EmployeeRecordSerializer, AdminSchoolSerializer, SchoolUpdateSerializer, SchoolSerializer,BalanceSerializer,PaymentSerializer, PaymentCreateSerializer
from .models import Admin, Schools, Balances ,Payment
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import NotFound

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = AdminUserCreationSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminView(generics.ListAPIView):
    queryset= Admin.objects.all()
    serializer_class= AdminSerializer
    
    
class AdminUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if request.user.is_admin or int(pk) == request.user.pk:
            try:
                user = Admin.objects.get(pk=pk)
                if pk == str(request.user.pk):
                    serializer = AdminUserCreationSerializer(user)
                else:
                    serializer = EmployeeRecordSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Admin.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "You are not authorized to view this page."}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, pk):
        if request.user.is_admin or int(pk) == request.user.pk:
            try:
                user = Admin.objects.get(pk=pk)
                if pk == str(request.user.pk):
                    serializer = EmployeeRecordSerializer(user, data=request.data, partial=True)
                else:
                    serializer = AdminUserCreationSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Admin.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "You are not authorized to view this page."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        if request.user.is_admin and int(pk) != request.user.pk:
            try:
                user = Admin.objects.get(pk=pk)
                user.delete()
                return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
            except Admin.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "You are not authorized to view this page."}, status=status.HTTP_401_UNAUTHORIZED)
class AdminUserCreationView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    model = Admin
    serializer_class = AdminUserCreationSerializer
    lookup_field = 'phone_number'

    def get_queryset(self):
        return Admin.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(phone_number=self.kwargs[self.lookup_field])
            return obj
        except Admin.DoesNotExist:
            raise NotFound('No admin with given credentials exists')
    
    
  
       
class AdminUserCreationViewAuthenticated(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_admin:
            serializer = AdminUserCreationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "You are not authorized to view this page."}, status=status.HTTP_401_UNAUTHORIZED)

class EmployeeRecordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        
            serializer = EmployeeRecordSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    ##STARTING FROM THIS POINT GOING DOWNWARDS ITS SCHOOLS VIEWS 
    
class SchoolUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        if request.user.role == 'school_head':
            try:
                school = Schools.objects.get(head=request.user)
                serializer = SchoolUpdateSerializer(school, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Schools.DoesNotExist:
                return Response({"error": "School not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "You are not authorized to view this page."}, status=status.HTTP_401_UNAUTHORIZED)

class AdminSchoolUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if request.user.is_admin:
            try:
                school = Schools.objects.get(pk=pk)
                serializer = AdminSchoolSerializer(school, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Schools.DoesNotExist:
                return Response({"error": "School not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "You are not authorized to view this page."}, status=status.HTTP_401_UNAUTHORIZED) 
    
    
    
class UpdateTermView(APIView):
    def post(self, request):
        current_term = get_current_term()
        current_year = get_current_year()
        schools = Schools.objects.all()
        for school in schools:
            previous_balance = Balances.objects.filter(school=school, term=current_term, year=current_year).first()
            if previous_balance:
                new_balance = calculate_new_balance(school, previous_balance.balance)
                Balances.objects.create(school=school, term=current_term, year=current_year, enrolment=school.enrolment, balance=new_balance)
        return Response({'message': 'Term updated successfully'})

def calculate_new_balance(school, previous_balance):
    if school.school_level == 'PRY':
        return (int(school.enrolment) * 2) + previous_balance
    elif school.school_level == 'SEC':
        return (int(school.enrolment) * 4) + previous_balance


class PaymentListView(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'id'

class PaymentBulkUploadView(APIView):
    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
            payments = []
            for row in reader:
                payment_data = {
                    'user': row['user'],
                    'amount': row['amount'],
                    'payment_method': row['payment_method']
                }
                serializer = PaymentCreateSerializer(data=payment_data)
                if serializer.is_valid():
                    payment = serializer.save()
                    payments.append(PaymentSerializer(payment).data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(payments, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class BalanceListView(ListAPIView):
    queryset = Balances.objects.all()
    serializer_class = BalanceSerializer

class BalanceDetailView(RetrieveAPIView):
    queryset = Balances.objects.all()
    serializer_class = BalanceSerializer
    lookup_field = 'id'

class SchoolBalanceView(APIView):
    def get(self, request, school_id):
        try:
            balances = Balances.objects.filter(school_id=school_id)
            serializer = BalanceSerializer(balances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)