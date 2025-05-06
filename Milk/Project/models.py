from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
class UserManager(BaseUserManager):
    def create_user(self, email, fullname, phone_number, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not fullname:
            raise ValueError("User must have a fullname")
        if not phone_number:
            raise ValueError("User must have a phone number")

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
            phone_number=phone_number,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, phone_number, password=None):
        user = self.create_user(email, fullname, phone_number, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12)
    date_joined = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'fullname'
    REQUIRED_FIELDS = ['email', 'phone_number']

    def __str__(self):
        return self.fullname

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
class Category(models.Model):
   name=models.CharField(max_length=30,unique=True,default='Milk')

   def __str__(self):
       return self.name
   
class Product(models.Model):
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    product_name=models.CharField(max_length=30)
    product_price=models.IntegerField()
    product_quantity=models.IntegerField()
    product_discount=models.IntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.product_name
class Addtocart(models.Model):
    customer_id=models.ForeignKey(User,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    price=models.PositiveIntegerField()
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product_id.product_price * self.quantity
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.customer_id.fullname} - {self.product_id.product_name} - {self.quantity}"
class Wishlist(models.Model):
    customer_id=models.ForeignKey(User,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.PositiveIntegerField()
    move_to_cart=models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product_id.product_price * self.quantity
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.customer_id.fullname} - {self.product_id.product_name} - {self.quantity}"

class PaymentMethod(models.TextChoices):
    CASH_ON_DELIVERY = 'COD', 'Cash on Delivery'
    UPI = 'UPI', 'UPI'

    
class Orders(models.Model):
    cart_id=models.ForeignKey(Addtocart,on_delete=models.CASCADE)
    address=models.TextField()
    phone_number=models.IntegerField(blank=True)
    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH_ON_DELIVERY,
    )
    def __str__(self):
        return str(f"{self.cart_id.customer_id.fullname}")