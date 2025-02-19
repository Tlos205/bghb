from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView

from countries.models import Country
from .models import DocumentType, DocumentFeature, FeatureDetail
from .forms import DocumentTypeForm, DocumentFeatureForm, FeatureDetailForm
from mixins.is_staff_mixin import IsStaffRequiredMixin
# Create your views here.


class DocumentTypeDetailView(DetailView):
    model = DocumentType
    template_name = 'documents/document_type_detail.html'
    context_object_name = 'document_type'  # Убедитесь, что объект доступен как `document`

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте дополнительные данные, если нужно
        return context


class DocumentTypeCreateView(IsStaffRequiredMixin, CreateView):
    model = DocumentType
    form_class = DocumentTypeForm
    template_name = 'documents/document_type_form.html'
    # success_url = '/documents/'  # Укажите URL для перенаправления после успешного создания

    def dispatch(self, request, *args, **kwargs):
        self.country_id = self.kwargs.get('country_id')  # Сохраняем country_id в атрибуте
        return super().dispatch(request, *args, **kwargs)


    def get_initial(self):
        initial = super().get_initial()
        initial['issuing_country'] = self.country_id  # Устанавливаем начальное значение для issuing_country
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['country'] = Country.objects.get(pk=self.country_id)  # Добавляем страну в контекст
        return context
    
    def get_success_url(self):
        # Перенаправляем на страницу деталей документа после его создания
        return reverse('documents:document_type_detail', kwargs={'pk': self.object.pk})
    

class DocumentFeatureCreateView(IsStaffRequiredMixin, CreateView):
    model = DocumentFeature
    form_class = DocumentFeatureForm
    template_name = 'documents/document_feature_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.document_id = self.kwargs.get('document_id')  # Сохраняем document_id в атрибуте
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['document_type'] = self.document_id  # Устанавливаем начальное значение для document_type
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document'] = DocumentType.objects.get(pk=self.document_id)  # Добавляем документ в контекст
        return context

    def form_valid(self, form):
        # Связываем особенность с документом
        self.object = form.save(commit=False)
        self.object.document_type_id = self.document_id  # Устанавливаем document_type_id
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Перенаправляем на страницу деталей документа после создания особенности
        return reverse('documents:document_type_detail', kwargs={'pk': self.document_id})


class FeatureDetailCreateView(IsStaffRequiredMixin, CreateView):
    model = FeatureDetail
    form_class = FeatureDetailForm
    template_name = 'documents/feature_detail_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.feature_id = self.kwargs.get('feature_id')  # Сохраняем feature_id в атрибуте
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['document_feature'] = self.feature_id  # Устанавливаем начальное значение для document_feature
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feature'] = DocumentFeature.objects.get(pk=self.feature_id)  # Добавляем особенность в контекст
        return context

    def form_valid(self, form):
        # Связываем деталь с особенностью
        self.object = form.save(commit=False)
        self.object.document_feature_id = self.feature_id  # Устанавливаем document_feature_id
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Перенаправляем на страницу деталей документа после создания детали
        feature = DocumentFeature.objects.get(pk=self.feature_id)
        return reverse('documents:document_type_detail', kwargs={'pk': feature.document_type.pk})


class DocumentTypeUpdateView(IsStaffRequiredMixin, UpdateView):
    model = DocumentType
    form_class = DocumentTypeForm
    template_name = 'documents/document_type_form.html'
    success_url = '/documents/'  # Укажите URL для перенаправления после успешного обновления

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['document_feature_form'] = DocumentFeatureForm(self.request.POST, 
                                                                   instance=self.object.features.first())
            context['feature_detail_form'] = FeatureDetailForm(self.request.POST, 
                                                               self.request.FILES, 
                                                               instance=self.object.features.first().details.first())
        else:
            context['document_feature_form'] = DocumentFeatureForm(instance=self.object.features.first())
            context['feature_detail_form'] = FeatureDetailForm(instance=self.object.features.first().details.first())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        document_feature_form = context['document_feature_form']
        feature_detail_form = context['feature_detail_form']

        if document_feature_form.is_valid() and feature_detail_form.is_valid():
            self.object = form.save()
            document_feature = document_feature_form.save(commit=False)
            document_feature.document_type = self.object
            document_feature.save()

            feature_detail = feature_detail_form.save(commit=False)
            feature_detail.document_feature = document_feature
            feature_detail.save()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
        

class DocumentFeatureUpdateView(IsStaffRequiredMixin, UpdateView):
    model = DocumentFeature
    form_class = DocumentFeatureForm
    template_name = 'documents/document_feature_form.html'
    context_object_name = 'feature'

    def get_success_url(self):
        # Перенаправляем на страницу деталей документа после редактирования
        return reverse('documents:document_type_detail', kwargs={'pk': self.object.document_type.pk})


class FeatureDetailUpdateView(UpdateView):
    model = FeatureDetail
    form_class = FeatureDetailForm
    template_name = 'documents/feature_detail_form.html'
    context_object_name = 'detail'

    def get_success_url(self):
        # Перенаправляем на страницу деталей документа после редактирования
        return reverse('documents:document_type_detail', kwargs={'pk': self.object.document_feature.document_type.pk})