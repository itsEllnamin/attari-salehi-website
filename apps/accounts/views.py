from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages as msg
from utils import create_random_code, send_sms
from .forms import RegisterForm, VerifyCodeForm
from .models import CustomUser


# =============================== Functions ==================================


def page_path(filename):
    return f"accounts/{filename}.html"


def partial_path(filename):
    return f"accounts/partials/{filename}.html"


# =============================== Pages ==================================


class RegisterView(View):
    template_name = page_path("register")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            mobile_number = cd["mobile_number"]
            activation_code = create_random_code(5)
            password = cd["password1"]

            CustomUser.objects.create_user(
                mobile_number=mobile_number,
                activation_code=activation_code,
                password=password,
            )
            msg.success(
                request,
                "اطلاعات شما ثبت شد و کد فعالسازی به شماره همراه شما ارسال گردید.",
                "success",
            )
            send_sms(
                mobile_number,
                f"کد فعالسازی حساب کاربری در عطاری صالحی: {activation_code}",
            )

            request.session["registered_user"] = {
                "mobile_number": mobile_number,
                "activation_code": activation_code,
            }

            return redirect("accounts:verify_code")

        msg.error(request, "اطلاعات وارد شده معتبر نمی‌باشد.", "danger")
        return render(request, self.template_name, {"form": form})


class VerifyCodeView(View):
    template_name = page_path("verify_code")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = VerifyCodeForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = VerifyCodeForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            activation_code = int(cd['activation_code'])

            if request.session.has_key("registered_user"):
                user_session = request.session["registered_user"]
                s_mobile_number = user_session["mobile_number"]
                s_activation_code = user_session["activation_code"]

            else:
                msg.warning(
                    request, "برای ثبت نام ابتدا اطلاعات زیر را وارد کنید", "warning"
                )
                return redirect("accounts:register")

            if  activation_code == s_activation_code :
                user = get_object_or_404(CustomUser, mobile_number=s_mobile_number)
                user.is_active = True
                user.activation_code = create_random_code(5)
                user.save()
                del user_session
                msg.success(
                    request,
                    "ثبت‌نام با موفقیت انجام شد",
                    "success",
                )

                return redirect("main:index")
            else:
                msg.error(request, "کد وارد شده صحیح نمی‌باشد", "danger")
                return render(request, self.template_name, {"form": form})

        msg.error(request, "اطلاعات وارد شده معتبر نمی‌باشد.", "danger")
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name= page_path('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            pass