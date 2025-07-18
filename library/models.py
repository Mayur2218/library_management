from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
# Create your models here.
class CustomUserModel(BaseUserManager):
    def create_user(self, email, name, phone_number, date_of_birth,user_type, password=None):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            phone_number = phone_number,
            date_of_birth = date_of_birth,
            user_type= user_type,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_superuser(self,email, name, phone_number, date_of_birth, password=None):
        user = self.create_user(
            email,
            name = name,
            phone_number= phone_number,
            date_of_birth= date_of_birth,
            password=password,
            user_type = 'admin',
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email address", unique=True, max_length=255)
    name = models.TextField(max_length=100)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    user_type = models.CharField(max_length=15, choices=[('admin','Admin'), ('customer', 'Customer')], default='customer')
    date_joined = models.DateField(null=True)

    objects = CustomUserModel()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phone_number','date_of_birth', 'user_type']

    def __str__(self):
        return f"{self.name}"
    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_superuser
    def has_module_perms(self, app_label):
        return self.is_admin or self.is_superuser
    @property
    def is_staff(self):
        return self.is_admin

class Customer(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, null=True)
    address = models.CharField()
    create_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='cover_images/', blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(blank=True, null=True, default=1)

    def __str__(self):
        return self.title

class Issue(models.Model):
    student = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_book = models.DateField()
    status = models.CharField(max_length=20, choices=[('Issued', 'Issued'), ('Returned', 'Returned')], default='Issued')

    def __str__(self):
        return f"{self.student.user.name}"
class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Transection(models.Model):
    customer = models.ForeignKey (Customer, on_delete=models.CASCADE)
    book = models.ForeignKey (Book, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=6)
    transection_type = models.CharField(max_length=20, choices=[('purchase','Purchase'),('issue','Issue')])
    transection_date = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
