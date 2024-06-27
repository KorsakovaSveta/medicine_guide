from django import forms
from .models import *
class BMIForm(forms.ModelForm):
    height = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'см'}), label='Рост')
    weight = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'кг'}), label='Вес')
    class Meta:
        model = Person
        fields = ['height', 'weight']

class ChildHeightForm(forms.ModelForm):
    sex = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'м/ж'}), label='Пол')
    mothers_height = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'см'}), label='Рост матери')
    fathers_height = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'см'}), label='Рост отца')
    class Meta:
        model = Child
        fields = ['sex','mothers_height', 'fathers_height']

class ParamsForMeldnaForm(forms.ModelForm):
    creatinine = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': '62-115 мкмоль/л'}), label='Креатинин')

    bilirubin = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': '5.13-32.49 мкмоль/л'}), label='Билирубин')

    serum_na = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': '136-145 ммоль/л'}), label='Натрий в сыворотке(Sodium serum)')

    inr = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': '0.8-1.2'}), label='Международное нормализованное отношение (МНО/INR)')
    hemodialysis_twice_in_week_prior =forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'да/нет'}), label='Гемодиализ 2 раза в неделю')
    class Meta:
        model = MELDParams
        fields = ['creatinine', 'bilirubin','serum_na', 'inr', 'hemodialysis_twice_in_week_prior']