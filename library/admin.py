from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUseAdmin
from .models import *
from .forms import CustomUserForm, CustomUserChangeForm, AddBookForm
from django.contrib.auth.models import Group
# Register your models here.
class CustomUserAdmin(BaseUseAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserForm
    list_display = ['name', 'email', 'phone_number', 'date_of_birth', 'is_admin', 'user_type']
    list_filter = ['is_admin']
    fieldsets = [
        (None, {"fields": ['email', 'password']}),
        ("Personal info", {"fields": ['name', 'phone_number', 'date_of_birth', 'user_type']}),
        ("Permissions", {"fields": ("is_admin", "is_superuser", "is_active", "groups", "user_permissions")}),
    ]
    add_fieldsets = [
        (None, {"classes": ["wide"], "fields": ["email", "name", "phone_number","date_of_birth", "password1", "password2"], },),
    ]
    ordering = ['email']
    search_fields = ['email','phone_number']
    filter_horizontal = []

admin.site.register(MyUser, CustomUserAdmin)
admin.site.unregister(Group)

class BookView(admin.ModelAdmin):
    form = AddBookForm
    list_display = ['title', 'author', 'price','total_copies','available_copies']
    list_filter = ['author']
    search_fields = ['title', 'author']
    filter_horizontal = []
    ordering = ['title']

class IssueView(admin.ModelAdmin):
    list_display = ['customer','book_id','issue_date','status']
    search_fields = ['book_id']

admin.site.register(Book, BookView)
admin.site.register(Issue, IssueView)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Transection)
admin.site.register(Notification)
