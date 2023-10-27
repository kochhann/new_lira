import re
from django.db import models
from django.utils import timezone
from django.urls import reverse
from core.models import (
    Base,
    HeadCompany
)


class EquipamentBrand(Base):
    id = models.AutoField("ID", primary_key=True, blank=False, null=False)
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', on_delete=models.PROTECT, blank=False,
                                   null=False)
    name = models.CharField("Nome", max_length=100, blank=True, null=True)

    def soft_delete(self):
        self.active = False
        self.deactivation_date = timezone.now()
        self.save()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'


class EquipamentType(Base):
    id = models.AutoField("ID", primary_key=True, blank=False, null=False)
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', on_delete=models.PROTECT, blank=False,
                                   null=False)
    brand = models.CharField("Marca", max_length=100, blank=True, null=True)
    model = models.CharField("Modelo", max_length=100, blank=True, null=True)
    price = models.DecimalField("Preço", max_digits=100, decimal_places=2, blank=True, null=True)

    def soft_delete(self):
        self.active = False
        self.deactivation_date = timezone.now()
        self.save()

    def __str__(self):
        return self.brand + ' ' + self.model

    class Meta:
        verbose_name = 'Tipo de equipamento'
        verbose_name_plural = 'Tipos de equipamento'


class Equipament(models.Model):
    STATUS = (
        (1, 'Disponível'),
        (2, 'Locado'),
        (3, 'Em manutenção'),
        (4, 'Perdido'),
    )
    id = models.AutoField("ID", primary_key=True, blank=False, null=False)
    owner_comp = models.ForeignKey(HeadCompany, verbose_name='Empresa', on_delete=models.PROTECT, blank=False,
                                   null=False)
    serial_number = models.CharField("Serial", max_length=100, blank=False, null=False)
    type = models.ForeignKey(EquipamentType, on_delete=models.PROTECT, blank=False, null=False)
    status = models.CharField("Status", max_length=2, choices=STATUS, blank=False, null=False)

    def soft_delete(self):
        self.active = False
        self.deactivation_date = timezone.now()
        self.save()

    def __str__(self):
        return self.serial_number
