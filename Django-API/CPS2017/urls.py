from django.conf.urls import url
from CPS2017 import views

urlpatterns = [
    url(r'', views.SVM, name='svm'),
]
