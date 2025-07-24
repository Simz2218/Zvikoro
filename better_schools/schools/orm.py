from .models import Admin

admin_user = Admin.objects.create_user(
    phone_number='1234567890',
    password='password123',
    first_name='John',
    surname='Doe',
    username='johndoe',
    bio='Admin bio',
    department='Admin'
)
admin_user.is_admin = True
admin_user.save()

print("Admin user created successfully!")
print("Admin user details:")
print(admin_user.phone_number)
print(admin_user.first_name)
print(admin_user.surname)
