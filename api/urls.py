from django.urls import path
from api import views


urlpatterns = [
   path(r'register-user', views.register_user),
   path(r'apply-loan', views.apply_loan),
   path(r'make-payment', views.make_payment),
   path(r'get-statement', views.get_statement)
]