from django.contrib import admin
from .models import User,Category,Product,Addtocart,Wishlist,Orders
#  Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Addtocart)
admin.site.register(Wishlist)
admin.site.register(Orders)