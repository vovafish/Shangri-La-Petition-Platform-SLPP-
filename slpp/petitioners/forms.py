from django import forms

class RegistrationForm(forms.Form):
    petitioner_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2',
            'placeholder': 'user@example.com'
        }),
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
        }
    )
    fullname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2'}),
        error_messages={
            'required': 'Full name is required.',
        }
    )
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2', 'type': 'date'}),
        error_messages={
            'required': 'Date of birth is required.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2'}),
        error_messages={
            'required': 'Password is required.',
        }
    )
    bioid = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2',
            'id': 'bioid'
        }),
        max_length=10,
        error_messages={
            'required': 'BioID is required.',
        }
    )

class LoginForm(forms.Form):
    petitioner_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2'})
    )

class PetitionForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
