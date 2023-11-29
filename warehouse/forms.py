import re
from django import forms
from django.utils.html import format_html
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    EquipamentType,
    Equipament
)


class EquipamentTypeForm(forms.ModelForm):
    price = forms.CharField(required=False)
    company = forms.IntegerField(required=False)

    class Meta:
        model = EquipamentType
        fields = ['brand', 'model']

    # this function will be used for the validation
    def clean(self):
        # data from the form is fetched using super function
        super(EquipamentTypeForm, self).clean()
        company = self.cleaned_data.get('company')
        brand = self.cleaned_data.get('brand')
        model = self.cleaned_data.get('model')
        try:
            check = EquipamentType.objects.get(brand=brand, model=model, owner_comp__pk=company)
        except ObjectDoesNotExist:
            return self.cleaned_data
        if check.active:
            self._errors['brand'] = self.error_class([
                f'Já existe um tipo cadastrado com mesma marca e modelo - {check}'])
        else:
            self._errors['brand'] = self.error_class([
                    format_html("Gostaria de reativar o modelo{}?<br>"
                                "<a href='{}'>SIM</a><br>"
                                "<a href='{}'>NÃO</a>",
                                check,
                                reverse('react_equipament_type', args=[check.pk]),
                                reverse('list_equipament_type')
                                )])
        # return any errors if found
        return self.cleaned_data


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Equipament
        fields = ['serial_number']
