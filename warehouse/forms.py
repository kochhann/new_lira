from django import forms
import re
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

        self._errors['brand'] = self.error_class([
            f'Já existe um tipo cadastrado com mesma marca e modelo - {check}'])
        # return any errors if found
        return self.cleaned_data


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Equipament
        fields = ['serial_number']
