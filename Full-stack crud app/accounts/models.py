from django.db import models
# Create your models here.


class Tag(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name


class Product(models.Model):
  CATEGORY = (
    ('Indoor','Indoor'),  
    ('Out door', 'Out door')
     
  )
  name = models.CharField(max_length = 100,null=True)
  category = models.CharField(null=True,choices = CATEGORY)
  price = models.DecimalField(max_digits=25,decimal_places=2)
  description = models.CharField(max_length=300, blank=True)
  date_created = models.DateTimeField(auto_now_add=True,null=True)
  tag = models.ManyToManyField(Tag)

  def __str__(self):
    return self.name


class Customer(models.Model):
  name = models.CharField(max_length=200)
  phone = models.CharField(max_length=20,null=True)
  email = models.CharField(max_length=25,null=True)
  date_created = models.DateField(auto_now_add=True, null=True)

  def __str__(self):
    return self.name

class Order(models.Model):
  STATUS = (
            ('Pending','Pending'),
            ('Out for delivery','Out for delivery'),
            ('Delivered','Delivered')
  )
  customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  date_created = models.DateTimeField(auto_now_add=True,null=True)
  status = models.CharField(max_length=200,choices=STATUS,null=True)

  def __str__(self):
    return self.product.name