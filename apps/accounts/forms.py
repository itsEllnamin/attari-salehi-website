from django import forms
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    error_messages = {
        "password_mismatch": _("گذرواژه‌ها با هم مطابقت ندارند."),
    }
    password1 = forms.CharField(
        label=_("گذرواژه"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("تکرار گذرواژه"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("برای تائید، گذرواژه قبلی را وارد کنید."),
    )

    class Meta:
        model = CustomUser
        fields = ('mobile_number', 'email', 'name', 'family')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("گذرواژه"),
        help_text=_(
            "گذرواژه‌ها به صورت خام نگهداری نمی‌شوند لذا راهی برای مشاهدهٔ گذرواژهٔ "
            'این کاربر وجود ندارد، اما می‌توانید آن را با <a href="../password/">این فرم</a> تغییر دهید '
        ),
    )

    class Meta:
        model = CustomUser
        fields = "__all__"
        exclude = ('last_login', 'datetime_joined', 'id', 'activation_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                f"../../{self.instance.pk}/password/"
            )
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )