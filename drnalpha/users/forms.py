from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label="Enter your email address",
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta:
        model = User
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.labels_small = True  # custom

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_unusable_password()

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    """ See: django.contrib.auth.forms.AuthenticationForm """

    email = forms.EmailField(
        label="Enter your email address",
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    error_messages = {
        "invalid_login": "Please enter a correct email address.",
        "inactive": "This account is inactive.",
    }

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.labels_small = True  # custom

    def clean(self):
        cleaned_data = super().clean()
        email = self.cleaned_data.get("email")

        if email is not None:
            try:
                self.user_cache = User.objects.get(email=email)

                if not self.user_cache.is_active:
                    raise ValidationError(
                        self.error_messages["inactive"],
                        code="inactive",
                    )
            except User.DoesNotExist:
                raise ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                )

        return cleaned_data

    def get_user(self):
        return self.user_cache
