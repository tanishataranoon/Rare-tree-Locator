from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, Profile
from django.contrib.auth import get_user_model

User = get_user_model()

# Custom Sign-Up Form
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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['full_name']
        user.user_type = self.cleaned_data['user_type']
        user.profession = self.cleaned_data.get('profession', '')
        if commit:
            user.save()
        return user

# Profile Update Form

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_pic",
            "profession",
            "bio",
            "phone",
            "linkedin",
            "instagram",
            "twitter",
            "personal_website",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
        # make all optional
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

# Password Change Form
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Current Password", "autocomplete": "current-password"}),
    )
    new_password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "New Password", "autocomplete": "new-password"}),
    )
    new_password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm New Password", "autocomplete": "new-password"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        # only validate if any password field is filled
        old = cleaned_data.get("old_password")
        new1 = cleaned_data.get("new_password1")
        new2 = cleaned_data.get("new_password2")

        if not (old or new1 or new2):
            # all empty, skip validation
            self.cleaned_data = {}
            return self.cleaned_data

        if not old or not new1 or not new2:
            raise forms.ValidationError("Please fill out all password fields to change your password.")
        return cleaned_data