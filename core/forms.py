from django import forms
import re
from django.core.exceptions import ObjectDoesNotExist
from .models import *


class OpUserForm(forms.ModelForm):
    name = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = OpUser
        exclude = '__all__'


class ContactForm(forms.ModelForm):
    company = forms.IntegerField(required=False)
    estado = forms.ModelMultipleChoiceField(queryset=State.objects.all())
    cidade = forms.ModelMultipleChoiceField(queryset=City.objects.all())
    street = forms.CharField(label='Rua')
    number = forms.CharField(label='Número')
    further_info = forms.CharField(label='Complemento', required=False)
    neighborhood = forms.CharField(label='Bairro')
    zip_code = forms.CharField(label='CEP')
    phone = forms.CharField(label='Telefone')
    email = forms.CharField(label='E-mail')


class CustomerForm(forms.ModelForm):
    company = forms.IntegerField(required=False)
    estado = forms.ModelMultipleChoiceField(queryset=State.objects.all())
    cidade = forms.ModelMultipleChoiceField(queryset=City.objects.all())
    street = forms.CharField(label='Rua')
    number = forms.CharField(label='Número')
    further_info = forms.CharField(label='Complemento', required=False)
    neighborhood = forms.CharField(label='Bairro')
    zip_code = forms.CharField(label='CEP')
    phone = forms.CharField(label='Telefone')
    email = forms.CharField(label='E-mail')

    class Meta:
        model = Customer
        fields = ['comp_id', 'name', 'type_of', 'corporate_name', 'state_subscription', 'city_subscription',
                  'site', 'observation']

    # this function will be used for the validation
    def clean(self):
        # data from the form is fetched using super function
        super(CustomerForm, self).clean()
        company = self.cleaned_data.get('company')
        cnpj = self.cleaned_data.get('comp_id')
        id = re.findall("\d+", cnpj)
        cnpj = ''.join(id)
        try:
            check = Customer.objects.get(comp_id=cnpj, owner_comp__pk=company)
        except ObjectDoesNotExist:
            return self.cleaned_data

        self._errors['comp_id'] = self.error_class([
                f'CNPJ / CPF já consta na sua base de clientes! - {check.name}'])
        # return any errors if found
        return self.cleaned_data


class SearchCustomerForm(forms.ModelForm):
    class Meta:
        model = SearchClass
        fields = ['search_param',]

