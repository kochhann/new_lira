import re
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.core import serializers
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    User,
    Group
)
from datetime import datetime
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
    View
)
from .models import (
    OpUser,
    Branch,
    Customer,
    City,
    State,
    Address,
    Telephone,
    Email
)
from .forms import (
    OpUserForm,
    CustomerForm
)


def load_cidades(request):
    depart = request.GET['outro_param']
    estado = State.objects.get(pk=depart)

    qs_json = serializers.serialize('json', estado.city_set.all())
    return HttpResponse(qs_json, content_type='application/json')


class IndexView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['doc_title'] = 'Home'
        return context


class LoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['doc_title'] = 'Autenticação'
        context['top_app_name'] = 'Autenticação'
        context['pt_h1'] = 'Login Lirasoft'
        context['pt_span'] = 'Entre com e-mail e senha'
        context['pt_breadcrumb2'] = 'Autenticação'
        return context


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        day = datetime.now().day
        month = datetime.now().month
        operador = False
        groups = self.request.user.groups.all()
        for i in groups:
            if i.name == 'Operadores':
                operador = True
        if self.request.user.is_staff or self.request.user.is_anonymous:
            context['doc_title'] = 'Dashboard'
            context['top_app_name'] = 'Switch'
            context['pt_h1'] = 'ACESSO AOS SERVIÇOS'
            context['pt_span'] = ''
            context['pt_breadcrumb2'] = 'Acesso a portais'
        if operador:
            aut = OpUser.objects.get(user=self.request.user)
            context['doc_title'] = 'Área do Usuário'
            context['top_app_name'] = 'Autorizações'
            context['pt_h1'] = 'Área do usuário'
            context['pt_span'] = 'Detalhes da sua conta'
            context['pt_breadcrumb2'] = 'Área do usuário'
        context['is_operador'] = operador
        return context


@method_decorator(login_required, name='dispatch')
class OpUserList(ListView):
    model = OpUser
    template_name = 'opuser_list.html'

    def get_context_data(self, **kwargs):
        context = super(OpUserList, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        users = OpUser.objects.filter(company=comp).order_by('user__first_name')
        context['doc_title'] = 'Gestão de usuários'
        context['top_app_name'] = 'Usuários'
        context['pt_h1'] = 'Gestão de usuários'
        context['pt_breadcrumb2'] = 'Usuários'
        context['users'] = users
        return context


@method_decorator(login_required, name='dispatch')
class OpUserCreate(CreateView):
    model = OpUser
    form_class = OpUserForm

    def get_context_data(self, **kwargs):
        context = super(OpUserCreate, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        branches = Branch.objects.filter(owner_comp=comp)
        context['company'] = comp.pk
        context['user'] = us.pk
        context['branches'] = branches
        context['doc_title'] = 'Gestão de usuários'
        context['top_app_name'] = 'Usuários'
        context['pt_h1'] = 'Gestão de usuários'
        context['pt_span'] = ''
        context['pt_breadcrumb2'] = 'Usuários'
        return context

    def form_valid(self, form, *args, **kwargs):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        new_operator = form.save(commit=False)
        name, *surname = name.split()
        surname = " ".join(surname)
        # # create user in auth system
        user = User.objects.create_user(email, email, surname)
        user.first_name = name
        user.last_name = surname
        user.save()
        ## add new operator user
        new_operator.user = user
        new_operator.active = True
        new_operator.save()
        # add in Operadores group
        g = Group.objects.get(name='Operadores')
        g.user_set.add(user)

        messages.success(self.request, 'Usuário criado com sucesso')
        return super(OpUserCreate, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro no cadastro: ' + str(form.errors))
        return super(OpUserCreate, self).form_invalid(form, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class CustomerList(ListView):
    model = Customer
    template_name = 'customer_list.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerList, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        customers = Customer.objects.filter(owner_comp=comp).order_by('name')
        context['doc_title'] = 'Gestão de clientes'
        context['top_app_name'] = 'Clientes'
        context['pt_h1'] = 'Gestão de clientes'
        context['pt_breadcrumb2'] = 'Clientes'
        context['customers'] = customers
        return context


@method_decorator(login_required, name='dispatch')
class CustomerCreate(CreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('list_customer')

    def get_context_data(self, **kwargs):
        context = super(CustomerCreate, self).get_context_data(**kwargs)
        states = State.objects.all()
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company.pk
        context['company'] = comp
        context['states'] = states
        context['doc_title'] = 'Gestão de clientes'
        context['top_app_name'] = 'Clientes'
        context['pt_h1'] = 'Gestão de clientes'
        context['pt_span'] = ''
        context['pt_breadcrumb2'] = 'Clientes'
        return context

    def form_valid(self, form, *args, **kwargs):
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company
        c_id = form.cleaned_data.get('comp_id')
        customer = form.save(commit=False)
        if len(c_id) < 18:
            customer.type_of = 2
        customer.owner_comp_id = comp.pk
        id = re.findall("\d+", customer.comp_id)
        customer.comp_id = ''.join(id)
        customer.save()
        ## Main address insert
        st = form.cleaned_data.get('estado')
        ct = form.cleaned_data.get('cidade')
        street = form.cleaned_data.get('street')
        for i in st:
            state = i
        for i in ct:
            city = i
        address = Address(
            name='Principal',
            owner_customer=customer,
            state=state,
            city=city,
            street=form.cleaned_data.get('street'),
            number=form.cleaned_data.get('number'),
            further_info=form.cleaned_data.get('further_info'),
            neighborhood=form.cleaned_data.get('neighborhood'),
            zip_code=form.cleaned_data.get('zip_code')
        )
        address.save()
        ## Main phone
        ph = form.cleaned_data.get('phone')
        l_full =  re.findall("\d+", ph)
        full = ''.join(l_full)
        ddd = full[:2]
        phone = full[2:len(full)]
        new_phone = Telephone(
            name='Principal',
            owner_customer=customer,
            code=ddd,
            number=phone
        )
        new_phone.save()
        ## Main e-mail
        new_mail = Email(
            name='Principal',
            owner_customer=customer,
            email=form.cleaned_data.get('email')
        )
        new_mail.save()
        messages.success(self.request, 'Cliente cadastrado com sucesso')
        return super(CustomerCreate, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        print(form.errors)
        # messages.error(self.request, 'Erro no cadastro: ' + str(form.errors))
        return super(CustomerCreate, self).form_invalid(form, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class CustomerView(DetailView):
    model = Customer

    def get_context_data(self, **kwargs):
        context = super(CustomerView, self).get_context_data(**kwargs)
        us = self.request.user
        op = OpUser.objects.get(user=us.pk)
        comp = op.company.pk
        # contratos = self.object.contract_set.all()
        # notas = self.object.billing_set.all()
        context['doc_title'] = 'Gestão de clientes'
        context['top_app_name'] = 'Clientes'
        context['pt_h1'] = 'Gestão de clientes'
        context['pt_breadcrumb2'] = 'Clientes'
        # context['contratos'] = contratos
        # context['notas'] = notas
        return context


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'email/change_password_link.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordView, self).get_context_data(**kwargs)
        context['doc_title'] = 'Acesso'
        context['top_app_name'] = 'Acesso'
        context['pt_h1'] = 'Acesso ao sistema Lirasoft'
        context['pt_span'] = 'Solicite uma recuperação de senha'
        context['pt_breadcrumb2'] = 'recuperar senha'
        return context

    def form_valid(self, form, *args, **kwargs):
        email = form.cleaned_data.get('email')
        User = get_user_model()
        users = User.objects.all()
        ck = False
        for u in users:
            if u.email == email:
                ck = True
        if ck:
            msg = 'Sua solicitação foi enviada com sucesso. Em alguns instantes você vai receber uma mensagem no ' \
                  'e-mail cadastrado com as instruções para alteração de senha'
            messages.success(self.request, msg)
            return super(ResetPasswordView, self).form_valid(form, *args, **kwargs)
        else:
            msg = 'O e-mail digitado não foi encontrado nos nossos registros. Por favor, confira o endereço digitado ' \
                  'e tente novamente'
            messages.error(self.request, msg)
            return super(ResetPasswordView, self).form_valid(form, *args, **kwargs)


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordConfirmView, self).get_context_data(**kwargs)
        context['doc_title'] = 'Acesso'
        context['top_app_name'] = 'Acesso'
        context['pt_h1'] = 'Acesso ao sistema Lirasoft'
        context['pt_span'] = 'Nova senha'
        context['pt_breadcrumb2'] = 'nova senha'
        return context


class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordCompleteView, self).get_context_data(**kwargs)
        context['doc_title'] = 'Acesso'
        context['top_app_name'] = 'Acesso'
        context['pt_h1'] = 'Acesso ao sistema Lirasoft'
        context['pt_span'] = 'Nova senha'
        context['pt_breadcrumb2'] = 'nova senha'
        return context
