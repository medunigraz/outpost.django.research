from django.conf.urls import include, url

from . import views

app_name = "research"

urlpatterns = [
    url(r"^search/$", views.SearchView.as_view()),
    url(r"^detail/$", views.DetailView.as_view()),
]
