from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .seriallizers import RegisterSerializer, LoginSerializer,ProductSeriallizer,AddtocartSeriallizer,CategorySeriallizer,WishlistSerializer,OrderSeriallizer
from .models import User,Product,Addtocart,Category,Wishlist,Orders
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
#<------------------------------Registration-------------------->
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = user.tokens()
            return Response({
                'message': "Registered successfully!",
                'refresh': refresh['refresh'],
                'access': refresh['access']
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data)

class RegisterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    lookup_field = 'pk'


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = user.tokens()
            return Response({
                'message': "Rara Battu ra!",
                'refresh': tokens['refresh'],
                'access': tokens['access']
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token is None:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Eyhase Nikloo"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Invalid token or token is expired."}, status=status.HTTP_400_BAD_REQUEST)
#<-----------------------------Categories-------------------------->
class CategoryView(APIView):
    def get(self,request):
        categories=Category.objects.all()
        serializer=CategorySeriallizer(categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=CategorySeriallizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class CategoryDetailview(APIView):
    def get_object(self,pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound("category with given id not exists")
    def get(self,request,pk):
        category=self.get_object(pk)
        serializer=CategorySeriallizer(category)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        category=self.get_object(pk)
        serializer=CategorySeriallizer(category,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        category=self.get_object(pk)
        category.delete()
        return Response("Category deleted succesfully")
#<-----------------------------------Products--------------------------------->
class ProductView(APIView):
    def get(self,request):
        products=Product.objects.all()
        serializer=ProductSeriallizer(products,many=True)
        return Response({
            'message':"vachay",
            "data":serializer.data
        })
    def post(self,request):
        serializer=ProductSeriallizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)
        
class ProductInDetailview(APIView):
    def get_object(self,pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound("Product with given  id does not exist")
    def get(self,request,pk):
        product=self.get_object(pk)
        serializer=ProductSeriallizer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        product=self.get_object(pk)
        serializer=ProductSeriallizer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        product=self.get_object(pk)
        product.delete()
        return Response("deleted succesfully")
#<-------------------Add to cart------------------->
class AddtocartView(APIView):
    def get(self, request):
        wishlist_items = Wishlist.objects.filter(move_to_cart=True)
        for item in wishlist_items:
            existing_cart_item = Addtocart.objects.filter(customer_id=item.customer_id,product_id=item.product_id).first()
            if existing_cart_item:
                existing_cart_item.quantity += item.quantity
                existing_cart_item.price += item.product_id.product_price * item.quantity
                existing_cart_item.save()
            else:
                Addtocart.objects.create(customer_id=item.customer_id,product_id=item.product_id,quantity=item.quantity,price=item.product.product_price * item.quantity)
            item.delete()
        cart_items = Addtocart.objects.all()
        serializer = AddtocartSeriallizer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer=AddtocartSeriallizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)
class AddtocartDetailView(APIView):
    def get_object(self,pk):
        try:
            return Addtocart.objects.get(pk=pk)
        except Addtocart.DoesNotExist:
            raise NotFound("Cart Details are not found with given id")
    def get(self,request,pk):
        cart=self.get_object(pk)
        serializer=AddtocartSeriallizer(cart)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        cart=self.get_object(pk)
        serializer=AddtocartSeriallizer(cart,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        cart=self.get_object(pk)
        cart.delete()
        return Response("Card is Deleted Succesfully")
#<----------------Wishlist---------------------->
class WishlistView(APIView):
    def get(self,request):
        wishlist=Wishlist.objects.all()
        # for wish in wishlist:
        #     if wish.move_to_cart:
        #         wish.delete()
        serializer=WishlistSerializer(wishlist,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=WishlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class WishlistDetailview(APIView):
    def get_object(self,pk):
        try:
            return Wishlist.objects.get(pk=pk)
        except Wishlist.DoesNotExist:
            return NotFound("Wishlist with given id does not exist")
    def get(self,request,pk):
        wishlist=self.get_object(pk)
        serializer=WishlistSerializer(wishlist)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        wishlist=self.get_object(pk)
        serializer=WishlistSerializer(wishlist,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        wishlist=self.get_object(pk)
        wishlist.delete()
        return Response("Wishlist Deleted Succesfully")
    
class CategoryProductsView(APIView):
    def get(self, request, name):
        category = get_object_or_404(Category, name=name)
        products = Product.objects.filter(category=category)
        serializer = ProductSeriallizer(products, many=True)
        all_names=[]
        for item in serializer.data:
            all_names.append(item['product_name'])
        return Response({
            "products": all_names
        })

# orders View 
class OrderView(APIView):
    def get(self,request):
        queryset=Orders.objects.all()
        serializer=OrderSeriallizer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=OrderSeriallizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)