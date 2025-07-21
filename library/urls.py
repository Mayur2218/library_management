from . import views
from django.urls import path
from .views import AdminOnlyLoginView

urlpatterns = [
    #authentication
    path('', AdminOnlyLoginView.as_view(), name='login'),
    path('customer_register/', views.customer_register, name='create_student'),
    path ('logout/', views.logout, name='logout'),

    #main body
    path ('about/', views.about, name='about'),
    path ('dashboard/', views.dashboard, name='dashboard'),

    #CRUD operations
    path ('book_details/', views.book_details, name='book_details'),
    path ('add_book/', views.add_book, name='add_book'),
    path ('update_book/<int:book_id>', views.update_book, name='update_book'),
    path ('remove_book/<int:book_id>', views.remove_book, name='remove_book'),

    #Issue
    path ('issue_book/', views.issue_book, name='issue_book'),
    path ('user_details/', views.user_details, name='user_details'),
    path ('buy_book/<int:book_id>/', views.buy_book, name='buy_book'),
    path ('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path ('checkout/', views.checkout, name='checkout'),

]
