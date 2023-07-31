from django import forms
from .models import PaymentType



class OrderForm(forms.Form):
    name = forms.CharField(label='', 
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
                           error_messages={'required':'این فیلد نمی‌تواند خالی بماند'}
                           )
    family = forms.CharField(label='', 
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام‌خانوادگی'}),
                           error_messages={'required':'این فیلد نمی‌تواند خالی بماند'}
                           )
    email = forms.CharField(label='', 
                           widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
                           error_messages=False
                           )
    phone_number = forms.CharField(label='', 
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تلفن'}),
                           error_messages=False
                           )
    address = forms.CharField(label='', 
                           widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'آدرس', 'rows':'2'}),
                           error_messages={'required':'این فیلد نمی‌تواند خالی بماند'}
                           )
    description = forms.CharField(label='', 
                           widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'توضیحات', 'rows':'3'}),
                           error_messages=False
                           )
    payment_type = forms.ChoiceField(label='', choices='', widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_type'].choices = PaymentType.payment_type_choices()

