from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('Login.html', views.Login, name="Login"), 
	       path('Register.html', views.Register, name="Register"),
	       path('Signup', views.Signup, name="Signup"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('AddProduct.html', views.AddProduct, name="AddProduct"),
	       path('AddProductAction', views.AddProductAction, name="AddProductAction"),
	       path('UpdateTracing.html', views.UpdateTracing, name="UpdateTracing"),
	       path('UpdateTracingAction', views.UpdateTracingAction, name="UpdateTracingAction"),
	       path('ViewTracing.html', views.ViewTracing, name="ViewTracing"),	
	       path('AddTracingAction', views.AddTracingAction, name="AddTracingAction"),
]