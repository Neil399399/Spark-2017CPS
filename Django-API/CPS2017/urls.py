from django.conf.urls import url
from CPS2017 import views

urlpatterns = [
    url(r'mutiClassification/motor', views.mutiClassification_motor, name='mutiClassification_motor'),
    url(r'mutiClassification/module', views.mutiClassification_module, name='mutiClassification_module'),
    url(r'environmental_info', views.environmental_information, name='environmental_information'),
]
