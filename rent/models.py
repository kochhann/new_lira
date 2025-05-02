from django.db import models
from django.utils import timezone
from django.urls import reverse
from core.models import (
    Base,
    HeadCompany,
    Branch,
    Issuer,
    Customer
)


class Contract(Base):
    TYPE_CHOICES = [
        (1, 'Mensal'),
        (2, 'Diário'),
    ]
    id = models.AutoField('ID', primary_key=True, blank=False, null=False)
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', on_delete=models.PROTECT, blank=False,
                                   null=False)
    branch = models.ForeignKey(Branch, verbose_name='Filial', on_delete=models.PROTECT, blank=True, null=True)
    issuer = models.ForeignKey(Issuer, verbose_name='Emissor', on_delete=models.PROTECT, blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name='Cliente', on_delete=models.PROTECT, blank=False, null=False)
    start_date = models.DateField('Início', blank=False, null=False)
    end_date = models.DateField('Fim', blank=True, null=True, default=None)
    delivery_date = models.DateField('Entrega', blank=True, null=True, default=None)
    type_of = models.IntegerField('Tipo', choices=TYPE_CHOICES, blank=False, null=False, default=1)
    observations = models.CharField('Observações', max_length=300)
    ticket = models.BooleanField('Boleto', blank=False, default=False)
    fee = models.DecimalField('Preço', max_digits=100, decimal_places=2)
    billing_day = models.CharField('Vencimento Boleto', max_length=10, blank=True, null=True)

    def soft_delete(self):
        self.active = False
        self.deactivation_date = timezone.now()
        self.save()

    def __str__(self):
        return f'#{self.id} - {self.customer.name}'

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
