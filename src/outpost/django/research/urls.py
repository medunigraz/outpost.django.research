from django.urls import (
    include,
    path,
)

from . import views

app_name = "research"

urlpatterns = [
    path("search/<str:database>/<str:schema>/", views.SearchView.as_view()),
    path("detail/<str:database>/<str:schema>/", views.DetailView.as_view()),
]
