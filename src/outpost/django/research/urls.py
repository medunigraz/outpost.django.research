from django.conf.urls import include, url

from . import views

app_name = "research"

urlpatterns = [
    url(r"^search/(?P<schema>\w+)/$", views.SearchView.as_view()),
    url(r"^detail/(?P<schema>\w+)/$", views.DetailView.as_view()),
]
