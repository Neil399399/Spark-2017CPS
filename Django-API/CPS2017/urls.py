from django.conf.urls import url
from CPS2017 import views

urlpatterns = [
<<<<<<< HEAD
    url(r'', views.mutiClassification, name='mutiClassification'),
    url(r'', views.mutiClassification, name='mold')
=======
    url(r'mutiClassification/motor', views.mutiClassification_motor, name='mutiClassification_motor'),
    url(r'mutiClassification/module', views.mutiClassification_module, name='mutiClassification_module'),
    url(r'environmental_info', views.environmental_information, name='environmental_information'),
>>>>>>> 57e50b5d77cb058159953fc6dad3279fa02d0ebf
]
