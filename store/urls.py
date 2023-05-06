from django.urls import path
from . import views

urlpatterns = [
	path('', views.storeH, name="storeH"),
	path('cart/', views.cart, name="cart"),
	path('payment/', views.payment, name="payment"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout_user, name='logout'),
    path('update_item/',views.update_item,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),
    

]