from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPES, required=True)
    profession = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2', 'user_type', 'profession']

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")
        profession = cleaned_data.get("profession")

        if user_type == "contributor" and not profession:
            self.add_error("profession", "Profession is required for contributors.")

        return cleaned_data
# Login form