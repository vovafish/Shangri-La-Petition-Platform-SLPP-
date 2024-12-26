from django import forms

class RegistrationForm(forms.Form):
    petitioner_email = forms.EmailField()
    fullname = forms.CharField(max_length=100)
    dob = forms.DateField()
    password = forms.CharField(widget=forms.PasswordInput())
    bioid = forms.CharField(max_length=10)

class LoginForm(forms.Form):
    petitioner_email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
