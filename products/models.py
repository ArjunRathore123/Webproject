from django.db import models
from accounts.models import CustomUser

# Create your models here.

# class Seller(models.Model):
#     user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
#     def __str__(self):
#         return f'{self.user.first_name}'
    
class Category(models.Model):
    category_image=models.ImageField(upload_to='image')
    category_name=models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
class Brand(models.Model):
    brand_image=models.ImageField(upload_to='image')
    brand_name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.brand_name


        
class Color(models.Model):
    color=models.CharField(max_length=50)

    def __str__(self):
        return self.color
    

class Product(models.Model):
    product_image=models.ImageField(upload_to='image')
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    color=models.ManyToManyField(Color)
    quantity=models.PositiveIntegerField(default=0)
    price=models.IntegerField()
    description=models.TextField()
    #seller=models.ForeignKey(Seller,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
    
class CartItem(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    date_added=models.DateTimeField(auto_now_add=True)
    
    def subtotal(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f"{self.quantity} x {self.product}"
    

class Order(models.Model):
    user=models.ForeignKey(CustomUser,blank=True,null=True,on_delete=models.SET_NULL)
    city=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    is_paid=models.BooleanField(default=False)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_signature=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} {}' .format(self.id,self.user.first_name,self.user.last_name)


    
class Wallet(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    balance=models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.first_name}'s  Buyer Wallet"

class AdminWallet(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    balance=models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.first_name} for Admin Wallet'
     
    
class SellerWallet(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    balance=models.IntegerField(default=0)
    def __str__(self):
        return f'{self.user.first_name} for Seller Wallet'
    

    
    
    
    
