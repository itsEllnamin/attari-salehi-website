from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages as msg
from django.contrib.auth import authenticate, login, logout
from utils import create_random_code, send_sms, partial_path, page_path
from .forms import RegisterForm, VerifyCodeForm, LoginForm, RememberPasswordForm, ChangePasswordForm
from .models import CustomUser



appname = 'accounts'
# =============================== Functions =================================

# =============================== Pages ==================================

class RegisterView(View):
    template_name = page_path(appname, "register")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
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
                'Code',
                mobile_number,
                f'{activation_code}'
            )

            request.session["registered_user"] = {
                "mobile_number": mobile_number,
                "activation_code": activation_code,
            }

            return redirect("accounts:verify_code")

        msg.error(request, "اطلاعات وارد شده معتبر نمی‌باشد.", "danger")
        return render(request, self.template_name, {"form": form})


class VerifyCodeView(View):
    template_name = page_path(appname, "verify_code")

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
                user = CustomUser.objects.get(mobile_number=s_mobile_number)
                user.is_active = True
                user.activation_code = create_random_code(5)
                user.save()
                if user_session.get('remember_password'):
                    return redirect('accounts:change_password')
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
    template_name= page_path(appname, 'login')

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
            cd = form.cleaned_data
            user = authenticate(username=cd['mobile_number'], password=cd['password'])
            
            if user is not None:
                msg.success(request, 'خوش آمدید', 'success')
                login(request, user)
                next_url = request.GET.get('next')
                if next_url is not None:
                    return redirect(next_url)
                return redirect('main:index')
            else:
                msg.error(request, 'حساب کاربری فعالی با شماره موبایل و گذرواژه‌ی وارد شده وجود ندارد.', 'danger')
                return render(request, self.template_name, {'form':form})
        else:
                msg.error(request, 'اطلاعات واردشده معتبر نیست.', 'danger')
                return render(request, self.template_name, {'form':form})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        shop_cart = request.session.get('shop_cart')
        logout(request)
        request.session['shop_cart'] = shop_cart
        msg.success(request, 'بدرود', 'success')
        return redirect('main:index')


class RememberPasswordView(View):
    template_name = page_path(appname, 'remember_password')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = RememberPasswordForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = RememberPasswordForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            try:
                user = CustomUser.objects.get(is_active=True, mobile_number=mobile_number)
                activation_code = create_random_code(5)
                send_sms(
                    'Code',
                    mobile_number,
                    f'{activation_code}'
                )
                user.activation_code = activation_code
                user.save()
                request.session["registered_user"] = {
                    "mobile_number": mobile_number,
                    "activation_code": activation_code,
                    'remember_password':True
                }
                msg.success(request, 'کد احراز هویت به شماره موبایل شما ارسال شد.', 'success')
                return redirect('accounts:verify_code')
            except CustomUser.DoesNotExist:
                msg.error(request, 'حساب کاربری فعالی با شماره موبایل وارد شده وجود ندارد.', 'danger')
                return render(request, self.template_name, {'form':form})   
        else:
                msg.error(request, 'اطلاعات واردشده معتبر نیست.', 'danger')
                return render(request, self.template_name, {'form':form})


class ChangePasswordView(View):
    template_name = page_path(appname, 'change_password')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            if request.session.has_key("registered_user"):
                mobile_number = (user_session:=request.session['registered_user']).get('mobile_number')
            try:
                user = CustomUser.objects.get(is_active=True, mobile_number=mobile_number)
                user.set_password(password)
                user.save()
                del user_session
                msg.success(request, 'گذرواژه‌ی شما با موفقیت تغییر یافت.', 'success')
                return redirect('accounts:login')
            except CustomUser.DoesNotExist:
                msg.error(request, 'حساب کاربری فعالی با شماره موبایل وارد شده وجود ندارد.', 'danger')
                return render(request, self.template_name, {'form':form})   
        else:
            msg.error(request, 'اطلاعات واردشده معتبر نیست.', 'danger')
            return render(request, self.template_name, {'form':form})
