from django.conf.urls import url
from CPS2017 import views

urlpatterns = [
    url(r'mutiClassification/motor', views.mutiClassification_motor, name='mutiClassification_motor'),
    url(r'mutiClassification/mold', views.mutiClassification_punch, name='mutiClassification_punch'),
]
