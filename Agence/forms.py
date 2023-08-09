from django import forms
from .models import Suite, Category

class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    adress = forms.CharField(max_length=250)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)    


class SuiteForm(forms.ModelForm):
    class Meta:
        category = forms.ModelChoiceField(queryset=Category.objects.all())
        
        model = Suite
        fields = [
            "name",
            "city",
            "category",
            "slug",
            "price",
            "image",
        ]    