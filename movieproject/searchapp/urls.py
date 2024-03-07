from . import views
from django.urls import path
from .views import SearchResult
app_name='searchapp'
urlpatterns = [

    path('search/',views.SearchResult,name='SearchResult'),

    ]