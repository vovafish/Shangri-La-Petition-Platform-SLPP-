from django import forms

class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2'})
    )

class ThresholdUpdateForm(forms.Form):
    signature_threshold = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2'}),
        min_value=1
    )

class PetitionResponseForm(forms.Form):
    response = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2'})
    )