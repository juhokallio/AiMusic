from django.conf.urls import url
from . import views


urlpatterns = [
    url("training/(\d+)$", views.training, name="piece_id"),
    url("training/(\d+)/save$", views.save_critic, name="piece_id"),
    url("music/(\d+).midi$", views.get_midi, name="composition_id"),
    url(r'^composer/(\d+)/compose$', views.compose, name="composer_id"),
    url("", views.main),
]
