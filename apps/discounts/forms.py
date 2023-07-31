from django import forms


class DiscountCodeForm(forms.Form):
    discount_code = forms.CharField(label='', 
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد تخفیف'}),
                           error_messages={'required':'این فیلد نمی‌تواند خالی بماند'}
                           )