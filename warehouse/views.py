from decimal import Decimal
from difflib import SequenceMatcher
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import ProtectedError
from django.db import IntegrityError
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
from .forms import EquipamentTypeForm


@method_decorator(login_required, name='dispatch')
class WarehouseIndexView(TemplateView):
    template_name = 'wh_index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(WarehouseIndexView, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        equipaments = comp.equipament_set.filter(active=True)
        accessories = comp.accessory_set.filter(active=True)
        available = equipaments.filter(status=1)
        unavailable = equipaments.filter(status=2)
        context['unavailable'] = len(unavailable)
        context['equipaments'] = len(equipaments)
        context['accessories'] = len(accessories)
        context['available'] = len(available)
        context['doc_title'] = 'Gestão de estoque'
        context['top_app_name'] = 'Tipos de equipamento'
        context['pt_h1'] = 'Gestão de estoque'
        context['pt_span'] = ''
        context['pt_breadcrumb2'] = 'warehouse'
        return context


@method_decorator(login_required, name='dispatch')
class EquipamentTypeList(ListView):
    model = EquipamentType
    template_name = 'eqtype_list.html'

    def get_context_data(self, **kwargs):
        context = super(EquipamentTypeList, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        eq_type = EquipamentType.objects.filter(active=True, owner_comp=comp).order_by('brand')
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
        company = op.company
        brands = company.equipamentbrand_set.filter(active=True)
        context['company'] = comp
        context['brands'] = brands
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
        et.brand = form.cleaned_data.get('brand')
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
        comp = op.company
        brands = comp.equipamentbrand_set.filter(active=True)
        equipaments = self.object.equipament_set.filter(active=True)
        count_eqpt = len(equipaments)
        available = len(equipaments.filter(status=1))
        unavailable = len(equipaments.filter(status=2))
        maintenance = len(equipaments.filter(status=3))
        lost = len(equipaments.filter(status=4))
        str_price = str(self.object.price)
        comp = op.company.pk
        context['brands'] = brands
        context['price'] = str_price[:-3]
        context['available'] = available
        context['unavailable'] = unavailable
        context['maintenance'] = maintenance
        context['lost'] = lost
        context['count_eqpt'] = count_eqpt
        context['doc_title'] = 'Gestão de equipamentos'
        context['top_app_name'] = 'Tipos de equipamentos'
        context['pt_h1'] = 'Gestão de equipamentos'
        context['pt_breadcrumb2'] = 'Tipos de equipamentos'
        return context


@method_decorator(login_required, name='dispatch')
class EquipamentTypeUpdate(View):
    def post(self, *args, **kwargs):
        et = EquipamentType.objects.get(id=self.kwargs['pk'])
        new_brand = EquipamentBrand.objects.get(pk=self.request.POST.get('brand'))
        new_model = self.request.POST.get('model', None)
        new_price = self.request.POST.get('price', None)
        result = Decimal(new_price.replace('.', '').replace(',', '.'))

        if et.brand != new_brand:
            et.brand = new_brand
            et.save()
        if et.model != new_model:
            et.model = new_model
            et.save()
        if et.price != result:
            et.price = result
            et.save()

        messages.info(self.request, f'Atualização bem sucedida')
        return HttpResponseRedirect(reverse('view_equipament_type', args=[et.pk]))


@method_decorator(login_required, name='dispatch')
class EquipamentTypeDelete(DeleteView):
    model = EquipamentType
    success_url = reverse_lazy('list_equipament_type')
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.soft_delete()
            messages.success(self.request, f'Modelo {self.object} Excluído')
            return HttpResponseRedirect(self.get_success_url() + '#tab-brands-list')
        except ProtectedError:
            messages.error(request, f'Não foi possível excluir {self.object}, pois existem equipamentos vinculados')
            return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class EquipamentTypeReactivation(View):
    def get(self, *args, **kwargs):
        eq = EquipamentType.objects.get(pk=self.kwargs['pk'])
        eq.reactivate()
        messages.success(self.request, f'Modelo {eq} reativado com sucesso')
        messages.warning(self.request, f'O preço atual ({eq.price}) pode estar desatualizado. Verifique')
        return HttpResponseRedirect(reverse('list_equipament_type'))


@method_decorator(login_required, name='dispatch')
class EquipamentBrandList(TemplateView):
    template_name = 'equipamentbrand_form.html'

    def get_context_data(self, **kwargs):
        context = super(EquipamentBrandList, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        brands = comp.equipamentbrand_set.filter(active=True)
        context['doc_title'] = 'Gestão de estoque'
        context['top_app_name'] = 'Marcas de equipamento'
        context['pt_h1'] = 'Gestão de estoque'
        context['pt_span'] = ''
        context['pt_breadcrumb2'] = 'Marcas de equipamento'
        context['brands'] = brands
        return context


@method_decorator(login_required, name='dispatch')
class EquipamentBrandCreate(View):
    def post(self, *args, **kwargs):
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        brands = comp.equipamentbrand_set.filter(active=True)
        name = self.request.POST.get('name', None)
        almost_brands = ''
        first_match = True
        for item in brands:
            ratio = SequenceMatcher(a=str.upper(item.name.strip()),b=str.upper(name.strip())).ratio()
            if ratio == 1.0:
                message = 'Você já possui uma marca com este nome'
                messages.error(self.request, message)
                return HttpResponseRedirect(reverse('list_equipament_brand'))
            if ratio > 0.69:
                if first_match:
                    first_match = False
                    almost_brands += f'{item.name}'
                else:
                    almost_brands += f', {item.name}'
        if len(almost_brands) > 0:
            if len(almost_brands) == 1:
                message = f'Você tem uma marca com um nome igual ou semelhante: {almost_brands}'
            else:
                message = f'Você tem algumas marcas com nomes iguais ou semelhantes: {almost_brands}'
            messages.info(self.request,  format_html("{}<br>"
                                                     "Para cadastrar mesmo assim, <a href='{}'>clique aqui</a>",
                                                     message,
                                                     reverse('create_almost_same_brand', kwargs={'new_brand':name})
                                                     )
                          )
            return HttpResponseRedirect(reverse('list_equipament_brand'))
        brand = EquipamentBrand(
            name=name,
            owner_comp=op.company
        )
        brand.save()

        messages.success(self.request, 'Nova marca cadastrada com sucesso')
        return HttpResponseRedirect(reverse('list_equipament_brand'))


@method_decorator(login_required, name='dispatch')
class EquipamentBrandAlmostSameCreate(View):
    def get(self, *args, **kwargs):
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        name = self.kwargs['new_brand']
        brand = EquipamentBrand(
            name=name,
            owner_comp=op.company
        )
        brand.save()

        messages.success(self.request, 'Nova marca cadastrada com sucesso')
        return HttpResponseRedirect(reverse('list_equipament_brand'))


@method_decorator(login_required, name='dispatch')
class EquipamentBrandDelete(DeleteView):
    model = EquipamentBrand
    success_url = reverse_lazy('list_equipament_brand')
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(self.request, f'Marca {self.object.name} excluída')
            return HttpResponseRedirect(self.get_success_url() + '#tab-brands-list')
        except ProtectedError:
            messages.error(request, f'Não foi possível excluir {self.object.name}, pois existem'
                                    f' modelos de equipamentos vinculados')
            return HttpResponseRedirect(self.get_success_url() + '#tab-brands-list')


@method_decorator(login_required, name='dispatch')
class EquipamentList(ListView):
    model = Equipament
    template_name = 'equipament_list.html'

    def get_context_data(self, **kwargs):
        context = super(EquipamentList, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        type = EquipamentType.objects.get(pk=self.kwargs['pk'])
        get_many = pk=self.kwargs['many']
        many = False
        if get_many == 1:
            many = True
        equipaments = Equipament.objects.filter(active=True,
                                                owner_comp=comp,
                                                type=type).order_by('serial_number')
        context['doc_title'] = 'Gestão de estoque'
        context['top_app_name'] = 'Equipamentos'
        context['pt_h1'] = 'Gestão de estoque'
        context['pt_span'] = ''
        context['pt_breadcrumb2'] = 'Equipamentos'
        context['equipaments'] = equipaments
        context['type'] = type
        context['many'] = many
        return context


@method_decorator(login_required, name='dispatch')
class EquipamentOneCreate(View):
    def post(self, *args, **kwargs):
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        serial_number = self.request.POST.get('dd_form_equipament_sn', None)
        type = EquipamentType.objects.get(pk=self.request.POST.get('dd_form_equipament_type', None))
        get_many = self.request.POST.get('check_if_many')
        many = 0
        if get_many:
            many = 1
        try:
            equipament = Equipament(
                owner_comp=op.company,
                serial_number=serial_number,
                type=type,
                status=1
            )
            equipament.save()
        except IntegrityError:
            messages.error(self.request, f'Já existe um equipamento cadastrado com este SN {serial_number}')
            return HttpResponseRedirect(reverse('list_equipament', args=[type.pk, many]))
        messages.success(self.request, 'Equipamento cadastrado com sucesso')
        return HttpResponseRedirect(reverse('list_equipament', args=[type.pk, many]))


@method_decorator(login_required, name='dispatch')
class EquipamentDelete(DeleteView):
    model = Equipament
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        messages.error(request, f'Executado')
        return HttpResponseRedirect(reverse('list_equipament', args=[self.object.type.pk, 0]))


@method_decorator(login_required, name='dispatch')
class AccessoryList(ListView):
    model = Accessory
    template_name = 'accessory_list.html'

    def get_context_data(self, **kwargs):
        context = super(AccessoryList, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        accept_similar = self.kwargs['similar']
        accessories = Accessory.objects.filter(active=True, owner_comp=comp)
        brands = comp.equipamentbrand_set.filter(active=True)
        context['doc_title'] = 'Gestão de estoque'
        context['top_app_name'] = 'Acessórios'
        context['pt_h1'] = 'Gestão de estoque'
        context['pt_span'] = ''
        context['pt_breadcrumb2'] = 'Acessórios'
        context['accessories'] = accessories
        context['brands'] = brands
        context['similar'] = accept_similar
        return context


@method_decorator(login_required, name='dispatch')
class AccessoryCreate(View):
    def post(self, *args, **kwargs):
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        accessories = comp.accessory_set.filter(active=True)
        new_brand = EquipamentBrand.objects.get(pk=self.request.POST.get('brand'))
        new_name = self.request.POST.get('name', None)
        new_price = self.request.POST.get('price', None)
        new_quantity = self.request.POST.get('quantity', 0)
        similar = self.request.POST.get('similar', None)
        result = Decimal(new_price.replace('.', '').replace(',', '.'))
        if similar == '0':
            almost_accessories = []
            for item in accessories:
                if item.brand == new_brand:
                    ratio = SequenceMatcher(a=str.upper(item.name.strip()), b=str.upper(new_name.strip())).ratio()
                    if ratio == 1.0:
                        message = f'Você já possui um acessório com este nome: {item}'
                        messages.error(self.request, message)
                        return HttpResponseRedirect(reverse('list_accessory', args=[0]))
                    if ratio > 0.69:
                        almost_accessories.append(item.name)
            if len(almost_accessories) > 0:
                if len(almost_accessories) == 1:
                    message = f'Você tem um acessório da mesma marca com um nome semelhante: {almost_accessories[0]}'
                else:
                    acc_list = ''
                    first = True
                    for i in almost_accessories:
                        if first:
                            acc_list = f'{i}'
                        else:
                            acc_list += f', {i}'
                    message = f'Você tem alguns acessórios da mesma marca com nomes iguais ou semelhantes: {acc_list}'
                messages.info(self.request,  format_html("{}<br>"
                                                     "Para cadastrar mesmo assim, <a href='{}'>clique aqui</a> e repita"
                                                         " a operação",
                                                     message,
                                                     reverse('list_accessory', args=[1])
                                                     )
                              )
                return HttpResponseRedirect(reverse('list_accessory', args=[0])

                                            )

        if similar == '1':
            for item in accessories:
                if item.brand == new_brand:
                    ratio = SequenceMatcher(a=str.upper(item.name.strip()), b=str.upper(new_name.strip())).ratio()
                    if ratio == 1.0:
                        message = f'Você já possui um acessório com este nome: {item}'
                        messages.error(self.request, message)
                        return HttpResponseRedirect(reverse('list_accessory', args=[0]))
        accessory = Accessory(
            owner_comp=comp,
            brand=new_brand,
            name=new_name,
            price=result,
            quantity=new_quantity
        )
        accessory.save()

        messages.info(self.request, f'Acessório cadastrado: {accessory}')
        return HttpResponseRedirect(reverse('list_accessory', args=[0]))


@method_decorator(login_required, name='dispatch')
class AccessoryQuantityUpdate(View):
    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        option = self.request.POST.get(f'gridRadios{pk}')
        accessory = Accessory.objects.get(pk=pk)
        new_quantity = self.request.POST.get(f'qtt{pk}')
        msg = ''
        if option == 'add':
            accessory.quantity += int(new_quantity)
            accessory.save()
            msg = f'Adicionados {new_quantity} itens'
        elif option == 'rem':
            if int(new_quantity) > accessory.quantity:
                messages.error(self.request, f'A quantidade a reduzir ({new_quantity}) é menor do que'
                                             f' a quantidade disponível ({accessory.quantity})')
                return HttpResponseRedirect(reverse('list_accessory', args=[0]))
            accessory.quantity -= int(new_quantity)
            accessory.save()
            msg = f'Removidos {new_quantity} itens'

        messages.info(self.request, f'Atualização bem sucedida. {msg}')
        return HttpResponseRedirect(reverse('list_accessory', args=[0]))


@method_decorator(login_required, name='dispatch')
class AccessoryDelete(DeleteView):
    model = Accessory
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        messages.error(request, f'Executado')
        return HttpResponseRedirect(reverse('list_accessory', kwargs={'similar':0}))
