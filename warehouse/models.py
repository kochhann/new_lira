import re
from django.db import models
from django.utils import timezone
from django.urls import reverse
from core.models import (
    Base,
    HeadCompany
)


class EquipamentBrand(Base):
    id = models.AutoField('ID', primary_key=True, blank=False, null=False)
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', on_delete=models.PROTECT, blank=False,
                                   null=False)
    name = models.CharField('Nome', max_length=100, blank=True, null=True)

    def soft_delete(self):
        self.active = False
        self.deactivation_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'


class EquipamentType(Base):
    id = models.AutoField('ID', primary_key=True, blank=False, null=False)
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', on_delete=models.PROTECT, blank=False,
                                   null=False)
    brand = models.ForeignKey(EquipamentBrand, verbose_name='Marca', on_delete=models.PROTECT, blank=False, null=False)
    model = models.CharField('Modelo', max_length=100, blank=True, null=True)
    price = models.DecimalField('Preço', max_digits=100, decimal_places=2, blank=True, null=True)

    def soft_delete(self):
        self.active = False
        self.deactivation_date = timezone.now()
        self.save()

    def reactivate(self):
        self.active = True
        self.deactivation_date = None
        self.save()

    def __str__(self):
        return self.brand.name + ' ' + self.model

    class Meta:
        verbose_name = 'Tipo de equipamento'
        verbose_name_plural = 'Tipos de equipamento'


class Equipament(Base):
    STATUS = (
        (1, 'Disponível'),
        (2, 'Locado'),
        (3, 'Em manutenção'),
        (4, 'Perdido'),
    )
    id = models.AutoField('ID', primary_key=True, blank=False, null=False)
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', on_delete=models.PROTECT, blank=False,
                                   null=False)
    serial_number = models.CharField('Serial', max_length=100, unique=True, blank=False, null=False)
    type = models.ForeignKey(EquipamentType, on_delete=models.PROTECT, blank=False, null=False)
    status = models.CharField('Status', max_length=2, choices=STATUS, blank=False, null=False)

    def soft_delete(self):
        self.active = False
        self.deactivation_date = timezone.now()
        self.save()

    def __str__(self):
        return self.serial_number

    class Meta:
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'


class Accessory(Base):
    id = models.AutoField('ID', primary_key=True, blank=False, null=False)
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', on_delete=models.PROTECT, blank=False,
                                   null=False)
    brand = models.ForeignKey(EquipamentBrand, verbose_name='Marca', on_delete=models.PROTECT, blank=False, null=False)
    name = models.CharField('Nome', max_length=200, blank=False, null=False)
    price = models.DecimalField('Preço', max_digits=100, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField('Quantidade', blank=False, null=False, default=0)

    def soft_delete(self):
        self.active = False
        self.deactivation_date = timezone.now()
        self.save()

    def reactivate(self):
        self.active = True
        self.deactivation_date = None
        self.save()

    def __str__(self):
        return f'{self.brand.name} {self.name}'

    class Meta:
        verbose_name = 'Acessório'
        verbose_name_plural = 'Acessórios'
