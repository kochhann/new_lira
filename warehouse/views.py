from decimal import Decimal
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    ListView,
    DetailView
)
from core.models import OpUser
from .models import EquipamentType
from .forms import EquipamentTypeForm


@method_decorator(login_required, name='dispatch')
class EquipamentTypeList(ListView):
    model = EquipamentType
    template_name = 'eqtype_list.html'

    def get_context_data(self, **kwargs):
        context = super(EquipamentTypeList, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        eq_type = EquipamentType.objects.filter(owner_comp=comp).order_by('brand')
        context['doc_title'] = 'Gestão de estoque'
        context['top_app_name'] = 'Tipos de equipamento'
        context['pt_h1'] = 'Gestão de estoque'
        context['pt_span'] = ''
        context['pt_breadcrumb2'] = 'Tipos de equipamento'
        context['eq_type'] = eq_type
        return context


@method_decorator(login_required, name='dispatch')
class EquipamentTypeCreate(CreateView):
    model = EquipamentType
    form_class = EquipamentTypeForm
    success_url = reverse_lazy('list_equipament_type')

    def get_context_data(self, **kwargs):
        context = super(EquipamentTypeCreate, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company.pk
        context['company'] = comp
        context['doc_title'] = 'Gestão de estoque'
        context['top_app_name'] = 'Tipos de equipamento'
        context['pt_h1'] = 'Gestão de estoque'
        context['pt_span'] = ''
        context['pt_breadcrumb2'] = 'Tipos de equipamento'
        return context

    def form_valid(self, form, *args, **kwargs):
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        price = form.cleaned_data.get('price')
        result = Decimal(price.replace('.', '').replace(',', '.'))
        et = form.save(commit=False)
        et.price = result
        et.owner_comp_id = comp.pk
        et.save()
        messages.success(self.request, 'Tipo de equipamento cadastrado com sucesso')
        return super(EquipamentTypeCreate, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        # print(form.errors)
        # messages.error(self.request, 'Erro no cadastro: ' + str(form.errors))
        return super(EquipamentTypeCreate, self).form_invalid(form, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class EquipamentTypeView(DetailView):
    model = EquipamentType

    def get_context_data(self, **kwargs):
        context = super(EquipamentTypeView, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company.pk
        context['doc_title'] = 'Gestão de equipamentos'
        context['top_app_name'] = 'Tipos de equipamentos'
        context['pt_h1'] = 'Gestão de equipamentos'
        context['pt_breadcrumb2'] = 'Tipos de equipamentos'
        return context
