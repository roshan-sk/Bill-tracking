from django import forms
from .models import Bill

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['name_of_item', 'description', 'price']