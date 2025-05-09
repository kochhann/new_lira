import re
import phonenumbers
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Base(models.Model):
    creation_date = models.DateField('Criação', auto_now_add=True)
    modification_date = models.DateField('Modificação', auto_now=True)
    deactivation_date = models.DateField('Desativado', blank=True, null=True, default=None)
    active = models.BooleanField('Ativo', default=True)

    class Meta:
        abstract = True


class Company(Base):
    id = models.AutoField('ID', primary_key=True, blank=False, null=False)
    accountable = models.CharField('Responsável', max_length=100, blank=True, null=True)
    accountable_id = models.CharField('CPF Responsável', max_length=20, blank=True, null=True)
    comp_id = models.CharField('CNPJ / CPF', max_length=20, blank=False, null=False)
    name = models.CharField('Nome', max_length=100, blank=False, null=False)
    corporate_name = models.CharField('Razão Social', max_length=100, blank=False, null=False)
    state_subscription = models.CharField('Inscricao Estadual', max_length=100, default='00000000',
                                          blank=True, null=True)
    city_subscription = models.CharField('Inscricao Municipal', max_length=100, default='00000000',
                                          blank=True, null=True)
    site = models.CharField('Site', max_length=100, default='não cadastrado', blank=True, null=True)
    observation = models.CharField('Observação', max_length=1000, blank=True, null=True)

    def soft_delete(self):
        self.active = False
        self.deactivation_date = timezone.now()
        self.save()

    @property
    def id_printable(self):
        if len(self.comp_id) < 14:
            return re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', self.comp_id)
        return re.sub(r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})', r'\1.\2.\3/\4-\5', self.comp_id)

    @property
    def acc_id_printable(self):
        if len(self.accountable_id) < 14:
            return re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', self.accountable_id)
        return re.sub(r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})', r'\1.\2.\3/\4-\5', self.accountable_id)

    class Meta:
        abstract = True


class HeadCompany(Company):
    class Meta:
        verbose_name = 'Matriz'
        verbose_name_plural = 'Matrizes'

    def __str__(self):
        return self.name


class Branch(Company):
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', on_delete=models.PROTECT, blank=False, null=False)

    class Meta:
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiais'

    def __str__(self):
        return self.name


class Issuer(Company):
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', on_delete=models.PROTECT, blank=False, null=False)

    class Meta:
        verbose_name = 'Emissora'
        verbose_name_plural = 'Emissoras'

    def __str__(self):
        return self.name


class Customer(Company):
    TYPE_CHOICES = [
        (1, 'Jurídica'),
        (2, 'Física'),
    ]
    type_of = models.IntegerField("Tipo", choices=TYPE_CHOICES, blank=False, null=False, default=1)
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', on_delete=models.PROTECT, blank=False, null=False)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.name


class OpUser(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.PROTECT, default=1, blank=False, null=False)
    company = models.ForeignKey(HeadCompany, verbose_name='Empresa', on_delete=models.PROTECT, default=1, blank=False, null=False)
    branch = models.ForeignKey(Branch, verbose_name='Filial', on_delete=models.PROTECT, default=1,
                              blank=True, null=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def send_login_mail(self):
        return self.user.name

    @property
    def name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    @property
    def last_login(self):
        return self.user.last_login

    @staticmethod
    def get_absolute_url():
        return reverse('list_user')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'Operador'
        verbose_name_plural = 'Operadores'


class Email(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField('Nome', max_length=100, blank=True, null=True)
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', blank=True, null=True,
                                   on_delete=models.SET_NULL)
    owner_branch = models.ForeignKey(Branch, verbose_name='Filial', blank=True, null=True,
                                     on_delete=models.SET_NULL)
    owner_issuer = models.ForeignKey(Issuer, verbose_name='Emissora', blank=True, null=True,
                                     on_delete=models.SET_NULL)
    owner_customer = models.ForeignKey(Customer, verbose_name='Cliente', blank=True, null=True,
                                       on_delete=models.SET_NULL)
    owner_user = models.ForeignKey(OpUser, verbose_name='Usuário', blank=True, null=True,
                                   on_delete=models.SET_NULL)
    email = models.EmailField('E-mail', blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'E-mail'
        verbose_name_plural = 'Endereços de e-mail'


class Telephone(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField('Nome', max_length=100, blank=True, null=True)
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', blank=True, null=True,
                                   on_delete=models.SET_NULL)
    owner_branch = models.ForeignKey(Branch, verbose_name='Filial', blank=True, null=True,
                                     on_delete=models.SET_NULL)
    owner_issuer = models.ForeignKey(Issuer, verbose_name='Emissora', blank=True, null=True,
                                     on_delete=models.SET_NULL)
    owner_customer = models.ForeignKey(Customer, verbose_name='Cliente', blank=True, null=True,
                                       on_delete=models.SET_NULL)
    owner_user = models.ForeignKey(OpUser, verbose_name='Usuário', blank=True, null=True,
                                   on_delete=models.SET_NULL)
    code = models.IntegerField('Código de área', blank=False, null=False)
    number = models.IntegerField('Número', blank=False, null=False)

    def __str__(self):
        return self.name

    @property
    def phone_printable(self):
        return phonenumbers.format_number(phonenumbers.parse(f'{self.code}{self.number}','BR'),
                                          phonenumbers.PhoneNumberFormat.NATIONAL)

    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'


class State(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False)
    name = models.CharField('Nome', max_length=100, blank=True, null=True)
    acronym = models.CharField('Sigla', max_length=2, blank=True, null=True)

    def __str__(self):
        return f'{self.name}({self.acronym})'


class City(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False)
    name = models.CharField('Nome', max_length=100, blank=True, null=True)
    ibge_code = models.IntegerField('IBGE', blank=False, null=False)
    state = models.ForeignKey(State, verbose_name='Estado', on_delete=models.CASCADE, blank=False, null=False)
    population_2010 = models.IntegerField('População (2010)', blank=False, null=False)
    density = models.DecimalField('Densidade', max_digits=8, decimal_places=2)
    ethnic = models.CharField('Gentílico', max_length=100, blank=True, null=True)
    area = models.DecimalField('Área', max_digits=12, decimal_places=3)

    def __str__(self):
        return f'{self.name} / {self.state.acronym}'


class Address(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField('Nome', max_length=100, blank=True, null=True)
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', blank=True, null=True,
                                   on_delete=models.SET_NULL)
    owner_branch = models.ForeignKey(Branch, verbose_name='Filial', blank=True, null=True,
                                     on_delete=models.SET_NULL)
    owner_issuer = models.ForeignKey(Issuer, verbose_name='Emissora', blank=True, null=True,
                                     on_delete=models.SET_NULL)
    owner_customer = models.ForeignKey(Customer, verbose_name='Cliente', blank=True, null=True,
                                       on_delete=models.SET_NULL)
    owner_user = models.ForeignKey(OpUser, verbose_name='Usuário', blank=True, null=True,
                                   on_delete=models.SET_NULL)
    state = models.ForeignKey(State, verbose_name='Estado', on_delete=models.PROTECT, blank=False, null=False)
    city = models.ForeignKey(City, verbose_name='Cidade', on_delete=models.PROTECT, blank=False, null=False)
    street = models.CharField('Rua', max_length=100, blank=False, null=False)
    number = models.CharField('Número', max_length=100, blank=False, null=False)
    further_info = models.CharField('Complemento', max_length=100, blank=True, null=True)
    neighborhood = models.CharField('Bairro', max_length=100)
    zip_code = models.CharField('CEP', max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'


class SearchClass(models.Model):
    search_param = models.CharField('Parametro', max_length=100, blank=True, null=True)
