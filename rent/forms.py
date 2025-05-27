from django import forms
import re
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Contract
)


class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = ['owner_comp','type_of','customer','observations','start_date']

    # this function will be used for the validation
    # def clean(self):
    #     # data from the form is fetched using super function
    #     super(CustomerForm, self).clean()
    #     company = self.cleaned_data.get('company')
    #     cnpj = self.cleaned_data.get('comp_id')
    #     id = re.findall("\d+", cnpj)
    #     cnpj = ''.join(id)
    #     try:
    #         check = Customer.objects.get(comp_id=cnpj, owner_comp__pk=company)
    #     except ObjectDoesNotExist:
    #         return self.cleaned_data
    #
    #     self._errors['comp_id'] = self.error_class([
    #             f'CNPJ / CPF já consta na sua base de clientes! - {check.name}'])
    #     # return any errors if found
    #     return self.cleaned_data
