from django.urls import path

from ads import views

urlpatterns = [
    path("", views.AdView.as_view()),
    path("<int:pk>/", views.AdDetailView.as_view()),
    path("data/", views.AdDataView.as_view())
]
