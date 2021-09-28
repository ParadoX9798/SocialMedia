from django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control",
                                                                            'placeholder': "Your Username"}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                                'placeholder': "Your Password"}))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                                            'placeholder': "Your Username"}))
    email = forms.EmailField(max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control",
                                                                            'placeholder': "Your Email"}))
    password1 = forms.CharField(label="Password", max_length=50,
                                widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                                 'placeholder': "Your Password"}))
    password2 = forms.CharField(label="Confirm Password", max_length=50,
                                widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                                 'placeholder': "Confirm Password"}))

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 != p2:
            raise forms.ValidationError("Passwords Doesn't Match!")

        email = cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError("Email Already in use!")
        user = cleaned_data.get('username')
        user = User.objects.filter(username=user)
        if user.exists():
            raise forms.ValidationError("Username Already in use")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'age')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-cotnrol'}),
        }
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))



