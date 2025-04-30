from django.urls import path
from .views import RegisterView,RegisterDetailView,LoginView,LogoutView,ProductView,ProductInDetailview,AddtocartView,AddtocartDetailView,CategoryView,WishlistView,WishlistDetailview,CategoryDetailview,CategoryProductsView,OrderView
urlpatterns = [
    path('Register/',RegisterView.as_view(),name='register'),
    path('Register/<int:pk>/',RegisterDetailView.as_view(),name='RegisterDetailview'),
    path('login/',LoginView.as_view(),name='loginview'),
    path('logout/',LogoutView.as_view(),name='LogoutView'),
    path('category/',CategoryView.as_view(),name='CategoryView'),
    path('category/<int:pk>',CategoryDetailview.as_view(),name='CategoryDetailview'),
    path('category/<str:name>/',CategoryProductsView.as_view(),name='CategoryProductsView'),
    path('product/',ProductView.as_view(),name='ProductView'),
    path('product/<int:pk>',ProductInDetailview.as_view(),name='ProductInDetailview'),
    path('cart/',AddtocartView.as_view(),name='AddtocartView'),
    path('cart/<int:pk>',AddtocartDetailView.as_view(),name='AddtocartDetailView'),
    path('wishlist/',WishlistView.as_view(),name='WishlistView'),
    path('wishlist/<int:pk>',WishlistDetailview.as_view(),name='WishlistDetailview'),
    path('orders/',OrderView.as_view(),name="OrderView")
]
