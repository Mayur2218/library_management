from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout

"""Navbar view and dashboard"""
@login_required
def about(request):
    return render(request, 'library/about.html')
@login_required
def dashboard(request):
    title = request.GET.get ('search', '')
    if title:
        books = Book.objects.filter (title__icontains=title).all ()
        if not books:
            messages.error (request, f"Search book are not available")
            return redirect ('dashboard')
    else:
        books = Book.objects.all ()
    return render(request, 'library/new_index.html', {"books":books,"search":title})

"""Authentication
Create User only register not login like(student only use library benefits not access they data) """
class AdminOnlyLoginView(LoginView):
    form_class = LoginForm
    template_name = 'library/login.html'
    def form_valid(self, form):
        user = form.get_user()
        if not(user.is_superuser or user.is_staff or user.is_active):
            messages.error(self.request,'Only admin can login')
            return redirect('login')
        return super().form_valid(form)

def customer_register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = MyUser.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                user_type='customer'
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # redirect to login or dashboard
    else:
        form = CustomerRegistrationForm()
    return render(request, 'library/register.html', {'form': form})

def create_student(request):
    if request.method == 'POST':
        form = NewStudentForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            enrollment = form.cleaned_data['enrollment_no']
            users = Customer.objects.filter(enrollment_no=enrollment).exists()
            if not users:
                new_user.save()
                return redirect('dashboard')
            else:
                messages.error(request, "Enrollment Number are already exists!")
    else:
            form = NewStudentForm()
    return render(request, 'library/register.html',{"form":form})
@login_required
def logout(request):
    django_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

"""CRUD (Add/ Issue/ Return Book)"""
@login_required
def book_details(request):
    books = Book.objects.all()
    return render(request, 'library/book_details.html', {"books":books})
@login_required
def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            addbook = form.save(commit=False)
            if addbook.available_copies is None:
                addbook.available_copies = addbook.total_copies
            addbook.save()
            return redirect('dashboard')
    else:
        form = AddBookForm()
    return render(request, 'library/add_book.html', {"form":form})
@login_required
def update_book(request, book_id):
    books = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = AddBookForm(request.POST, request.FILES,instance=books)
        if form.is_valid():
            form.save()
            messages.success(request, "Book data update successfully")
            return redirect('dashboard')
    else:
        form = AddBookForm(instance=books)
    return render(request, 'library/add_book.html',{"form":form})
@login_required
def remove_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    messages.success(request, 'Book are remove successfully')
    return redirect('book_details')

""" Book Issue, Return and Fine """
@login_required
def issue_book(request):
    if request.method == "POST":
        form = IssueBookForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            book = form.cleaned_data["book"]
            if book.available_copies > 0:
                book.available_copies -= 1
                book.save()
                issue.save()
                return redirect('dashboard')
            else:
                messages.error(request, "Book copies are not available!")
    else:
        form = IssueBookForm()
    return render(request, 'library/issue_book.html', {"form":form})
@login_required
def buy_book(request, book_id):
    books = get_object_or_404(Book, pk=book_id)
    return render(request, 'library/buy_book.html', {"books":books})
@login_required
def user_details(request):
    users = Customer.objects.all ()
    return render(request, 'library/user_details.html', {'users':users})

@login_required
def read_book(request):
    pass