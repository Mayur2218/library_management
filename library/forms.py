from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import *

class CustomUserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    class Meta:
        model = MyUser
        fields = ["name", "email", "phone_number", "date_of_birth"]

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Enter password are Not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = MyUser
        fields = ["name", "email", "password", "phone_number", "date_of_birth", "is_active", "is_admin", "is_superuser"]

class CustomerRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password != confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'title': forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Enter book name'}),
            'author': forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Enter book author name'}),
            'cover': forms.FileInput (attrs={'class': 'form-control'}),
            'price': forms.NumberInput (attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'description': forms.Textarea (attrs={'class': 'form-control', 'row':2,'placeholder': 'Enter book description (300 words)'}),
            'total_copies': forms.NumberInput (attrs={'class': 'form-control', 'placeholder': 'Enter Total Number of copies'}),
            'available_copies': forms.NumberInput (attrs={'class': 'form-control', 'placeholder': 'Enter same as above total copies'}),
        }

class IssueBookForm(forms.ModelForm):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label='Select Book',widget=forms.Select(attrs={'class':'form-select'}))
    class Meta:
        model = Issue
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'return_book': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter return date'}),
        }

class NewStudentForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Enter your fullname'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your EmailId'}),
            'phone_number': forms.NumberInput (attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea (attrs={'class': 'form-control', 'placeholder': 'Enter your current address', 'row':2}),
        }

class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter email','autocomplete':'off'}))
    password = forms.CharField(max_length=150, widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password','autocomplete':'off'}))
    def confirm_login_allowed(self, user):
        if not(user.is_superuser or user.is_staff):
            raise forms.ValidationError("Only admin users can login!", code="invalid_login")