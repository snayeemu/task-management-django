from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User, Group, Permission
from django import forms
from django.core.exceptions import ValidationError
import re
from tasks.forms import StyledFormMixin
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2", "email"]

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].help_text = "" 

class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User 
        fields = ["username", "first_name", "last_name", "password1", "confirm_password", "email"]

    def clean_password1(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        errors = []
        if len(password1) < 8:
            errors.append("Password must be at least 8 character long")
        if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password1):
            errors.append("Password must include uppercase, lowercase and special character")
        if len(errors):
            raise ValidationError(errors)
        return password1
    
    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        errors = []
        email_exist = User.objects.filter(email=email)
        if email_exist:
            errors.append("Email already exist!!")
            raise ValidationError(errors)
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password1 != confirm_password:
            raise ValidationError("Confirm password do not match")
        return cleaned_data 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        
    
class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

class AssignRoleForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset = Group.objects.all(),
        empty_label="Select a Role"
    )

class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permission"
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]