from django.contrib import admin
from .models import DocumentType, DocumentFeature, FeatureDetail
from countries.models import Country

import nested_admin


class FeatureDetailInline(nested_admin.NestedStackedInline):  # или admin.StackedInline
    model = FeatureDetail
    extra = 1  # Количество пустых форм для добавления новых деталей
    fields = ('key', 'value', 'image')  # Поля, которые будут отображаться в inline-форме


class DocumentFeatureInline(nested_admin.NestedStackedInline):  # или admin.StackedInline
    model = DocumentFeature
    extra = 1  # Количество пустых форм для добавления новых особенностей
    fields = ('feature_name',)  # Поля, которые будут отображаться в inline-форме
    inlines = [FeatureDetailInline]  # Вложенные inline-формы для FeatureDetail


class DocumentTypeInline(nested_admin.NestedStackedInline):  # или admin.StackedInline
    model = DocumentType
    extra = 1  # Количество пустых форм для добавления новых типов документов
    fields = ('code', 
              'name', 
              'category', 
              'type',
              'first_issue_date',
              'valid',
              'legal_status',
              'length',
              'width',
              'pages',
              'validity_period',
              'renewable',
              )  # Поля, которые будут отображаться в inline-форме
    inlines = [DocumentFeatureInline]  # Вложенные inline-формы для DocumentFeature


@admin.register(DocumentType)
class DocumentTypeAdmin(nested_admin.NestedModelAdmin):
    list_display = ('code', 'name', 'category', 'type', 'issuing_country')
    list_filter = ('issuing_country', 'category', 'type')
    search_fields = ('code', 'name', 'category')
    inlines = [DocumentFeatureInline]  # Вложенные inline-формы для DocumentFeature

@admin.register(DocumentFeature)
class DocumentFeatureAdmin(nested_admin.NestedModelAdmin):
    list_display = ('feature_name', 'document_type')
    list_filter = ('document_type',)
    search_fields = ('feature_name',)
    inlines = [FeatureDetailInline]  # Вложенные inline-формы для FeatureDetail

@admin.register(FeatureDetail)
class FeatureDetailAdmin(nested_admin.NestedModelAdmin):
    list_display = ('key', 'value', 'document_feature')
    list_filter = ('document_feature',)
    search_fields = ('key', 'value')