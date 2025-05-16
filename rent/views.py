from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    View,
    TemplateView,
    DeleteView
)
from core.models import OpUser
from .models import *
from .forms import ContractForm


@method_decorator(login_required, name='dispatch')
class RentIndexView(TemplateView):
    template_name = 'rent_index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(RentIndexView, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        context['doc_title'] = 'Gestão de locações'
        context['top_app_name'] = 'Contratos'
        context['pt_h1'] = 'Gestão de locações'
        context['pt_span'] = ''
        context['pt_breadcrumb2'] = 'locações'
        return context


@method_decorator(login_required, name='dispatch')
class ContractCreate(CreateView):
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy('rent_index')

    def get_context_data(self, **kwargs):
        context = super(ContractCreate, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        cust_id = self.kwargs['cust_id']
        customer = Customer.objects.get(id=cust_id)
        type_of = self.kwargs['type_of']
        to_txt = ''
        comp = op.company
        if type_of == 3:
            to_txt = 'Contrato Inativo'
        else:
            if type_of == 1:
                to_txt = 'Contrato Mensal'
            else:
                to_txt = 'Contrato de Diária'
        context['company'] = comp
        context['doc_title'] = 'Gestão de locações'
        context['top_app_name'] = 'Contratos'
        context['pt_h1'] = 'Gestão de locações'
        context['pt_span'] = ''
        context['pt_breadcrumb2'] = 'locações'
        context['type_of'] = to_txt
        context['type_of_n'] = type_of
        context['customer'] = customer
        return context

    # def form_valid(self, form, *args, **kwargs):
    #     us = self.request.user
    #     op = OpUser.objects.get(user=us.pk)
    #     comp = op.company
    #     c_id = form.cleaned_data.get('comp_id')
    #     customer = form.save(commit=False)
    #     if len(c_id) < 18:
    #         customer.type_of = 2
    #     customer.owner_comp_id = comp.pk
    #     id = re.findall("\d+", customer.comp_id)
    #     customer.comp_id = ''.join(id)
    #     customer.save()
    #     ## Main address insert
    #     st = form.cleaned_data.get('estado')
    #     ct = form.cleaned_data.get('cidade')
    #     street = form.cleaned_data.get('street')
    #     for i in st:
    #         state = i
    #     for i in ct:
    #         city = i
    #     address = Address(
    #         name='Principal',
    #         owner_customer=customer,
    #         state=state,
    #         city=city,
    #         street=form.cleaned_data.get('street'),
    #         number=form.cleaned_data.get('number'),
    #         further_info=form.cleaned_data.get('further_info'),
    #         neighborhood=form.cleaned_data.get('neighborhood'),
    #         zip_code=form.cleaned_data.get('zip_code')
    #     )
    #     address.save()
    #     ## Main phone
    #     ph = form.cleaned_data.get('phone')
    #     l_full =  re.findall("\d+", ph)
    #     full = ''.join(l_full)
    #     ddd = full[:2]
    #     phone = full[2:len(full)]
    #     new_phone = Telephone(
    #         name='Principal',
    #         owner_customer=customer,
    #         code=ddd,
    #         number=phone
    #     )
    #     new_phone.save()
    #     ## Main e-mail
    #     new_mail = Email(
    #         name='Principal',
    #         owner_customer=customer,
    #         email=form.cleaned_data.get('email')
    #     )
    #     new_mail.save()
    #     messages.success(self.request, 'Cliente cadastrado com sucesso')
    #     return super(CustomerCreate, self).form_valid(form)
    #
    # def form_invalid(self, form, *args, **kwargs):
    #     print(form.errors)
    #     # messages.error(self.request, 'Erro no cadastro: ' + str(form.errors))
    #     return super(CustomerCreate, self).form_invalid(form, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ContractList(ListView):
    model = Contract
    template_name = 'contract_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContractList, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        type_of = self.kwargs['type_of']
        to_txt = ''
        comp = op.company
        if type_of == 3:
            contracts = Contract.objects.filter(owner_comp=comp, active=False).order_by('id')
            to_txt = 'Contratos Inativos'
        else:
            contracts = Contract.objects.filter(owner_comp=comp, type_of=type_of, active=True).order_by('id')
            if type_of == 1:
                to_txt = 'Contratos Mensais'
            else:
                to_txt = 'Diárias'
        context['doc_title'] = 'Gestão de locações'
        context['top_app_name'] = 'Contratos'
        context['pt_h1'] = 'Gestão de locações'
        context['pt_span'] = ''
        context['pt_breadcrumb2'] = 'locações'
        context['contracts'] = contracts
        context['type_of'] = to_txt
        context['type_of_n'] = type_of
        return context
