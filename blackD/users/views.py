from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, LoginForm
from django.views import View
from django.contrib.auth import authenticate, login
import datetime

class UsersV(View):

    @staticmethod
    def login_view(request):
        form = LoginForm(request.POST or None)

        msg = None

        if request.method == "POST":

            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("home")
                    # if user.profile.is_trial:
                    #     if user.profile.is_paid == False:
                    #         date_joined= user.date_joined
                    #         now = datetime.datetime.now()
                    #         date = now - date_joined
                    #         if date.days < 7:
                    #             return redirect("home")
                    #         else:
                    #             user.is_blocked = True
                    #             messages.warning(request, f"You must pay to keep using this app")
                    #             return redirect("PAYMENT PAGE")
                else:
                    msg = 'Dados de usuário ou senha incorretos.'
            else:
                msg = 'Erro ao validar o formulário.'

        return render(request, "users/login.html", {"form": form, "msg": msg})

    @staticmethod
    def register(request):
        msg = None
        success = False

        if request.method == "POST":
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)

                success = True

                # return redirect("/login/")

            else:
                msg = 'Erro ao registrar-se.'
        else:
            form = UserRegisterForm()

        return render(request, "users/register.html", {"form": form, "msg": msg, "success": success})

    @staticmethod
    def register2(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'POST':                
                pform = ProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user.profile)
                if  pform.is_valid():
                    
                    pform.save()
                    username = pform.cleaned_data.get('username')
                    messages.success(request, f'Welcome to our family!')
                    return redirect('home')
            else:                
                pform = ProfileUpdateForm()
            context={           
            'pform':pform,
            }
            return render(request, 'users/register2.html', context)
        else:
            return redirect('register')

    @login_required
    def profile(request):
        if request.method == 'POST':
                          
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('profile')
               
            
            context = {
                'u_form': u_form,
                'p_form': p_form
            }
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
            context = {
                'u_form': u_form,
                'p_form': p_form
            }

        return render(request, 'users/profile.html', context)