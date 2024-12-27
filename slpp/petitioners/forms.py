from django import forms

class RegistrationForm(forms.Form):
    petitioner_email = forms.EmailField(
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
        }
    )
    fullname = forms.CharField(
        error_messages={
            'required': 'Full name is required.',
        }
    )
    dob = forms.DateField(
        error_messages={
            'required': 'Date of birth is required.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password is required.',
        }
    )
    bioid = forms.CharField(
        max_length=10,
        error_messages={
            'required': 'BioID is required.',
        }
    )

class LoginForm(forms.Form):
    petitioner_email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
