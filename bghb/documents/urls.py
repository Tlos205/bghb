from django.urls import path
from .views import *

app_name = 'documents'

urlpatterns = [

    path('<int:pk>/', DocumentTypeDetailView.as_view(), name='document_type_detail'),
    path('<int:country_id>/document-type/add/', DocumentTypeCreateView.as_view(), name='document_type_add'),
    path('document-type/<int:document_id>/feature/add/', DocumentFeatureCreateView.as_view(), name='document_feature_add'),
    path('feature/<int:pk>/edit/', DocumentFeatureUpdateView.as_view(), name='document_feature_edit'),
    path('feature/<int:feature_id>/detail/add/', FeatureDetailCreateView.as_view(), name='feature_detail_add'),
    path('detail/<int:pk>/edit/', FeatureDetailUpdateView.as_view(), name='feature_detail_edit'),
]