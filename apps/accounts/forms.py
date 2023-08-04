from django import forms
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import RegexValidator
from middlewares.middlewares import RequestMiddleware



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
            'این کاربر وجود ندارد، اما می‌توانید آن را با <a href="{}">این فرم</a> تغییر دهید '
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


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('mobile_number',)
        widgets = {
            "mobile_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "شماره موبایل را وارد کنید",
                }
            ),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'گذرواژه را وارد کنید'

        self.fields['password2'].help_text = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'تکرار گذرواژه را وارد کنید'
        

class VerifyCodeForm(forms.Form):
    activation_code_validator = RegexValidator(
    regex=r"^\d{5}$", message="کد احراز هویت یک عدد ۵ رقمی می‌باشد."
    )
    activation_code = forms.CharField(
        label="",
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "کد دریافتی را وارد کنید", "autofocus": True}
        ),
        validators=[activation_code_validator]
    )


class LoginForm(forms.Form):
    mobile_number_validator = RegexValidator(
    regex=r"^09\d{9}", message="شماره موبایل وارد شده معتبر نیست."
    )
    
    mobile_number = forms.CharField(
        label="شماره موبایل",
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "شماره موبایل را وارد کنید"}
        ),
        validators=[mobile_number_validator]
    )
    password = forms.CharField(
        label="گذرواژه",
        strip=False,
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "گذرواژه را وارد کنید"}
        ),
    )


class RememberPasswordForm(forms.Form):
    mobile_number_validator = RegexValidator(
    regex=r"^09\d{9}", message="شماره موبایل وارد شده معتبر نیست."
    )
    
    mobile_number = forms.CharField(
        label="شماره موبایل",
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "شماره موبایل را وارد کنید"}
        ),
        validators=[mobile_number_validator]
    )


class ChangePasswordForm(AdminPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        user = request.user
        super().__init__(user, *args, **kwargs)
        
        self.fields['password1'].help_text = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'گذرواژه را وارد کنید'

        self.fields['password2'].help_text = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'تکرار گذرواژه را وارد کنید'


class UpdateProfileForm(forms.Form):
    mobile_number = forms.CharField(
        label="شماره موبایل",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "شماره موبایل را وارد کنید", 'readonly': 'readonly'})
    )
    name = forms.CharField(
        label="نام",
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام را وارد کنید"})
    )
    family = forms.CharField(
        label="نام خانوادگی",
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام خانوادگی را وارد کنید"})
    )
    email = forms.EmailField(
        label="ایمیل",
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ایمیل را وارد کنید"})
    )
    phone_number = forms.CharField(
        label="شماره تلفن",
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "شماره تلفن را وارد کنید"})
    )
    address = forms.CharField(
        label="آدرس",
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "آدرس را وارد کنید", 'rows':'3'})
    )
    image = forms.ImageField(required=False)