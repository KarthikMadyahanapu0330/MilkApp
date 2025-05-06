from rest_framework import serializers
from .models import User,Product,Addtocart,Category,Wishlist,Orders
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'phone_number']
    def create(self, validated_data):
        return User.objects.create_user(
            fullname=validated_data['fullname'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
class LoginSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    password = serializers.CharField(write_only=True)
    class Meta:
        fields = ['fullname', 'password']
    def validate(self, data):
        fullname = data.get('fullname')
        password = data.get('password')
        try:
            user = User.objects.get(fullname=fullname)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")
        if not user.is_active:
            raise serializers.ValidationError("Account is inactive")
        data['user'] = user
        return data
#-----------------------Categories------------------------>
class CategorySeriallizer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name']
#-----------------------Products------------------------>
class ProductSeriallizer(serializers.ModelSerializer):
    product_price=serializers.IntegerField()
    category_name=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=['id','product_name','product_price','product_quantity','product_discount','category','category_name']
        read_only_fields=['category_name']
    def get_product_price(self, obj):
        return obj.product_price 
    def validate_product_price(self,data):
        if data<=0:
            raise serializers.ValidationError("price should be in Positive values")
        return data
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
#----------------------Add to cart------------------------>
class AddtocartSeriallizer(serializers.ModelSerializer):
    customer_name=serializers.SerializerMethodField()
    product_name=serializers.SerializerMethodField()
    quantity = serializers.IntegerField(required=True)
    class Meta:
        model=Addtocart
        fields=['id','customer_id','customer_name','product_id','product_name','quantity','price']
        read_only_fields=['customer_name','product_name','price']
    def get_customer_name(self, obj):
        if obj.customer_id:
            return obj.customer_id.fullname 
        else:
            return None
    def get_product_name(self, obj):
        if obj.product_id:
            return obj.product_id.product_name 
        else:
            return None
        
    def create(self,validated_data):
        product_id=validated_data['product_id']
        quantity=validated_data['quantity']
        customer_id=validated_data['customer_id']
        existing_item=Addtocart.objects.filter(customer_id=customer_id,product_id=product_id).first()
        if existing_item:
            if quantity>0:
                existing_item.quantity+=quantity
                existing_item.price=existing_item.product_id.product_price * existing_item.quantity
                existing_item.save()
                return existing_item
            elif quantity<0:
                existing_item.quantity += quantity
                existing_item.price = existing_item.product_id.product_price * existing_item.quantity
                existing_item.save()
                return existing_item
        else:
            validated_data['price']=product_id.product_price * quantity
            return Addtocart.objects.create(**validated_data)
    def update(self,instance,validated_data):
        instance.customer_id=validated_data['customer_id']
        instance.quantity=validated_data['quantity']
        instance.product_id=validated_data['product_id']
        instance.price=instance.product_id.product_price * instance.quantity
        instance.save()
        return instance
#<----------------------------Wishlist----------------------------->
class WishlistSerializer(serializers.ModelSerializer):
    customer_name=serializers.SerializerMethodField()
    product_name=serializers.SerializerMethodField()
    class Meta:
        model=Wishlist
        fields=['id','customer_id','customer_name','product_id','product_name','quantity','price','move_to_cart']
        read_only_fields=['customer_name','product_name','price']
    def get_customer_name(self,obj):
        if obj.customer_id:
            return obj.customer_id.fullname
        else:
            return None
    def get_product_name(self,obj):
        if obj.product_id:
            return obj.product_id.product_name
        else:
            return None
    def create(self,validated_data):
        product_id=validated_data['product_id']
        quantity=validated_data['quantity']
        move_to_cart=validated_data['move_to_cart']
        customer_id=validated_data['customer_id']
        existing_item=Wishlist.objects.filter(customer_id=customer_id,product_id=product_id).first()
        if existing_item:
            if quantity>0:
                existing_item.quantity+=quantity
                existing_item.price=existing_item.product_id.product_price * existing_item.quantity
                existing_item.save()
                return existing_item
            elif quantity<0:
                existing_item.quantity += quantity
                existing_item.price = existing_item.product_id.product_price * existing_item.quantity
                existing_item.save()
                return existing_item
        else:
            validated_data['price']=product_id.product_price * quantity
            return Wishlist.objects.create(**validated_data)
        if move_to_cart:
            item=Addtocart.objects.filter(customer_id=customer_id,product_id=product_id).first()
            if item:
                if quantity>0:
                    item.quantity+=quantity
                    item.price=item.product_id.product_price * item.quantity
                    item.save()
                elif quantity<0:
                    if item.quantity + quantity < 0:
                        raise ValueError("Quantity cannot go below zero.")
                    item.quantity += quantity
                    item.price = item.product_id.product_price * item.quantity
                    item.save()
                    return item
            else:
                validated_data['price']=product_id.product_price * quantity
                return Addtocart.objects.create(**validated_data)
        else:
            validated_data['price']=product_id.product_price * quantity
            return Addtocart.objects.create(**validated_data)
    def update(self,instance,validated_data):
        instance.customer_id=validated_data['customer_id']
        instance.quantity=validated_data['quantity']
        instance.product_id=validated_data['product_id']
        instance.move_to_cart=validated_data['move_to_cart']
        instance.price=instance.product_id.product_price * instance.quantity
        instance.save()
        return instance
    
class OrderSeriallizer(serializers.ModelSerializer):
    customer_id=serializers.SerializerMethodField()
    customer_name=serializers.SerializerMethodField()
    product_name=serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    price=serializers.SerializerMethodField()
    class Meta:
        model=Orders
        fields=['id','cart_id','address','phone_number','payment_method','customer_id','customer_name','product_name','quantity','price',"created_at"]
        read_only_fields=['customer_name','customer_id','product_name','quantity','price']
    def get_customer_id(self,obj):
        if obj.cart_id:
            return obj.cart_id.customer_id_id
        else:
            return None
    def get_customer_name(self,obj):
        if obj.cart_id:
            return obj.cart_id.customer_id.fullname
        else:
            return None
    def get_product_name(self,obj):
        if obj.cart_id:
            return obj.cart_id.product_id.product_name
        return None
    def get_quantity(self,obj):
        if obj.cart_id:
            return obj.cart_id.quantity
    def get_price(self,obj):
        if obj.cart_id:
            return obj.cart_id.price