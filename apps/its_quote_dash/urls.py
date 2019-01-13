from django.urls import path
from . import views 
urlpatterns = [
    path('', views.login),
    path('signup', views.register),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('add', views.add),
    path('like/<int:user_id>/<int:quote_id>', views.like),
    path('myaccount/<int:user_id>',views.edit),
    path('user/<int:user_id>',views.show),
    path('delete/<int:quote_id>',views.delete),
    
]
