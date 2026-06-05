from django import forms
from .models import B2BInquiry

class B2BInquiryForm(forms.ModelForm):
    # Hidden honeypot field for anti-spam protection
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label="Do not fill this out if you are human"
    )

    class Meta:
        model = B2BInquiry
        fields = [
            'company_name', 'country', 'email', 'phone',
            'requested_products', 'packaging_format', 'quantity', 'custom_message'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Acme Food Importers'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. France'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. buyer@acmefood.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +33 1 23 45 67 89'}),
            'requested_products': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Vinaigre blond d’alcool, Hot Sauce'}),
            'packaging_format': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5L, 1000L IBC'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1 FCL (Full Container Load)'}),
            'custom_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your import needs, delivery destination, OEM private labeling specifications...'}),
        }
