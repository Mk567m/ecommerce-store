from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm
class OrderForm(ModelForm):
  
  class Meta:
    model = Order
    fields = ['customer','product','status']


class CustomerForm(ModelForm):
  
  class Meta:
    model = Customer
    fields = ['name','phone','email']    

class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['first_name','last_name','username','email','password1','password2']    

class ForgotpasswordForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username','password1','password2']
