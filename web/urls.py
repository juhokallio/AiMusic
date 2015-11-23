from django.conf.urls import url
from . import views

urlpatterns = [
    url("training", views.training),
    url(r'^composer/(\d+)/compose$', views.compose, name="composer_id"),
    url("", views.main),
]
