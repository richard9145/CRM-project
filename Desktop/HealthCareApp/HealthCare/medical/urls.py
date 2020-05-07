from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views



app_name = 'medical'

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),


    path('products/', views.products, name='products'),
    path('user/', views.userPage, name='user-page'),
    
    path('account/', views.accountSettings, name='account'),
    path('customer/<str:cust>', views.customer, name='customer'),
    

    path('createcust', views.CustomerCreation, name='createcust'),
    path('order_form/<str:co>/', views.CreateOrder, name='order_form'),
    path('update_form/<str:uf>/', views.UpdateOrder, name='update_form'),
    path('delete_form/<str:do>/', views.deleteOrder, name='delete_form'),

    # path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete")

    # path('reset_password/',
    #     auth_views.PasswordResetView.as_view(template_name="medical/password_reset.html"), name="reset_password"),

    # path('reset_password_sent/', 
    #     auth_views.PasswordResetDoneView.as_view(template_name="medical/password_reset_sent.html"), name="password_reset_done"),

    # path('reset/<uidb64>[0-9A-Za-z]+)-<token>/',
    #     auth_views.PasswordResetConfirmView.as_view(template_name="medical/password_reset_form.html"), name="password_reset_confirm"),

    # path('reset_password_complete/', 
    #     auth_views.PasswordResetCompleteView.as_view(template_name="medical/password_reset_done.html"), name="password_reset_complete"),

]


