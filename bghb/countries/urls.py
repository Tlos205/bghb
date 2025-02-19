from django.urls import path
from .views import CountryListView, CountryDetailView, CountryCreateView, CountryUpdateView

# namespaces = 'countries'
app_name = 'countries'  

urlpatterns = [
    path('', CountryListView.as_view(), name='country_list'),
    path('<int:pk>/', CountryDetailView.as_view(), name='country_detail'),
    path('create/', CountryCreateView.as_view(), name='country_create'),
    path('<int:pk>/update/', CountryUpdateView.as_view(), name='country_update'),
]