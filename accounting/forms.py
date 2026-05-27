from django import forms


class SubtractQuantityForm(forms.Form):
    amount = forms.IntegerField(
        label='Количество',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите количество',
            'min': '1'
        })
    )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError('Количество должно быть больше 0')
        return amount