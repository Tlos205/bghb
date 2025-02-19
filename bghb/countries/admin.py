from django.contrib import admin
from .models import Country, EntryRegime
from documents.admin import DocumentTypeInline, DocumentFeatureInline, FeatureDetailInline

import nested_admin

admin.site.register(EntryRegime)

@admin.register(Country)
class CountryAdmin(nested_admin.NestedModelAdmin):
    list_display = ('short_name', 'code_3')
    search_fields = ('short_name', 'code_3')
    inlines = [DocumentTypeInline,] 