from django.db import models


# Create your models here.

class Dress(models.Model):
    dress_id = models.AutoField(primary_key=True)
    vendor_name=models.CharField(max_length=50,default="Khadis")
    dress_name=models.CharField(max_length=50,default="bridal dress")
    category=models.CharField(max_length=30,default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=3000)
    colours=models.CharField(max_length=50)
    size=models.CharField(max_length=50)
    quantity=models.IntegerField(default=0)
    material=models.CharField(max_length=100)
    stitching=models.CharField(max_length=19)
    contact=models.CharField(max_length=12)
    image=models.ImageField(upload_to="shoppage/images",default="")
    def __str__(self):
        return self.dress_name

class Quickform(models.Model):
    dress_name=models.CharField(max_length=15)
    dress_id=models.IntegerField(default=0)
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    phonenumber=models.CharField(max_length=11)
    city=models.CharField(max_length=10)
    state=models.CharField(max_length=10,default="pakistan")
    zipcode=models.IntegerField(default=0)
    def __str__(self):
        return self.name
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=30,default="")
    number=models.CharField(max_length=30)
    desc=models.CharField(max_length=3000)
    def __str__(self):
        return self.name
class Userdetails(models.Model):
    userid = models.AutoField(primary_key=True)
    email=models.EmailField(max_length=30,default="")
    password=models.CharField(max_length=20)
    status=models.CharField(max_length=8)
    def __str__(self):
        return self.status
class Orders (models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=5000)
    name=models.CharField(max_length=90)
    amount=models.IntegerField(default=0)
    email=models.EmailField(max_length=90)
    address=models.CharField(max_length=90)
    city=models.CharField(max_length=90)
    state=models.CharField(max_length=90)
    zip_code=models.CharField(max_length=10)
    phonenumber=models.CharField(max_length=10,default="")