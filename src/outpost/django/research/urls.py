from django.conf.urls import (
    include,
    url,
)

from . import views

app_name = "research"

urlpatterns = [
    url(
        r"^search/(?P<database>[\w\-.]+)/(?P<schema>\w+)/$", views.SearchView.as_view()
    ),
    url(
        r"^detail/(?P<database>[\w\-.]+)/(?P<schema>\w+)/$", views.DetailView.as_view()
    ),
]
