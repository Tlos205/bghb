from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Country, EntryRegime
from .forms import CountryForm, EntryRegimeForm

from mixins.is_staff_mixin import IsStaffRequiredMixin

from documents.models import DocumentType


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['country_count'] = Country.objects.count()
        context['document_type_count'] = DocumentType.objects.count()
        context['entry_regime_count'] = EntryRegime.objects.count()
        return context


class CountryListView(ListView):
    model = Country
    template_name = 'countries/country_list.html'
    context_object_name = 'countries'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')  # Получаем поисковый запрос
        if query:
            # Ищем по полному и краткому названию страны
            return Country.objects.filter(
                Q(full_name__icontains=query) | Q(short_name__icontains=query)
            )
        return Country.objects.all()  # Если запроса нет, возвращаем все страны


class CountryDetailView(DetailView):
    model = Country
    template_name = 'countries/country_detail.html'
    context_object_name = 'country'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entry_regimes'] = EntryRegime.objects.filter(country=self.object)
        return context


class CountryCreateView(IsStaffRequiredMixin, CreateView):
    model = Country
    form_class = CountryForm
    template_name = 'countries/country_form.html'
    success_url = reverse_lazy('countries:country_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['entry_regime_form'] = EntryRegimeForm(self.request.POST)
        else:
            context['entry_regime_form'] = EntryRegimeForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        entry_regime_form = context['entry_regime_form']
        if entry_regime_form.is_valid():
            self.object = form.save()
            entry_regime = entry_regime_form.save(commit=False)
            entry_regime.country = self.object
            entry_regime.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class CountryUpdateView(IsStaffRequiredMixin, UpdateView):
    model = Country
    form_class = CountryForm
    template_name = 'countries/country_form.html'
    # success_url = reverse_lazy('countries:country_detail')
    def get_success_url(self):
        # Получаем только что обновленный объект
        return reverse('countries:country_detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['entry_regime_form'] = EntryRegimeForm(self.request.POST, 
                                                           instance=self.object.entryregime_set.first()
                                                           )
        else:
            context['entry_regime_form'] = EntryRegimeForm(instance=self.object.entryregime_set.first())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        entry_regime_form = context['entry_regime_form']
        if entry_regime_form.is_valid():
            self.object = form.save()
            entry_regime = entry_regime_form.save(commit=False)
            entry_regime.country = self.object
            entry_regime.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
        

