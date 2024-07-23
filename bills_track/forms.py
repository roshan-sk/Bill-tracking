from django import forms
from .models import Bill
import datetime

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['name_of_item', 'description', 'price']

class SelectMonthYearForm(forms.Form):
    current_year = datetime.datetime.now().year
    bill_years = Bill.objects.dates('created_at', 'year', order='DESC')
    year_choices = [(year.year, year.year) for year in bill_years]
    month_choices = [(i, datetime.date(2000, i, 1).strftime('%B')) for i in range(1, 13)]

    year = forms.ChoiceField(choices=year_choices, label="Select Year")
    month = forms.ChoiceField(choices=month_choices, label="Select Month")  