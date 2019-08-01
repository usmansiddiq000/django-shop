from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

payment_choises = (
    ('P', 'paypal'),
    ('S', 'stripe')
)

class address_form(forms.Form):
    email = forms.EmailField(widget = forms.TextInput(
        attrs= {'placeholder': 'youremail@example.com', 'class': 'form-control'}
    ))
    address = forms.CharField(widget = forms.TextInput(
        attrs= {'placeholder': '1234 Main St', 'class': 'form-control'}
    ))
    country = CountryField(blank_label='select country').formfield(
        required=True,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    zip = forms.CharField(widget = forms.TextInput(
        attrs= {'class': 'form-control'}
    ))
    use_for_next_time = forms.BooleanField(widget= forms.CheckboxInput(), required=False)
    payment_method = forms.ChoiceField(widget = forms.RadioSelect(), choices= payment_choises)

