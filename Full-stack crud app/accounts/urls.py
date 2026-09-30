from django.urls import path

from . import views
urlpatterns = [
  path('',views.dashboard,name='home'),
  path('logout/',views.logoutpage,name='logout'),
  path('login/',views.loginpage,name='login'),
  path('register/',views.registerpage,name='register'),
  path('customer/<str:pkey>',views.customer,name='customer'),
  path('product/',views.product,name='product'),
  path('all_customers',views.all_customers,name="all_products"),
  path('create_order/<str:pk>',views.CreateOrder,name='create_order'),
  path('create_customer',views.CreateCustomer,name='create_customer'),
  path('delete_order/<str:pk>',views.DeleteOrder,name='delete_order'),
  path('update_order/<str:pk>',views.UpdateOrder,name='update_order'),
  path('update_customer/<str:pk>',views.UpdateCustomer,name="update_customer"),
  path('delete_customer/<str:pk>',views.DeleteCustomer,name="delete_customer"),
  path('forgotpassword/<int:user_id>',views.forgotpassword,name='forgotpassword')

]