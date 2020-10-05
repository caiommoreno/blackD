from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views import View
from django.contrib.auth import authenticate, login

class UsersV(View):


    @staticmethod
    def register(request):
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            
            if form.is_valid() :
                newUser = form.save()
                newUser = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
                login(request, newUser)
                
                username = form.cleaned_data.get('username')
                messages.success(request, f' welcome {username} Your account has been created! You can update your profile')
                return redirect('register2')
        else:
            form = UserRegisterForm()
            
        context={
        'form': form,
        
        }
        return render(request, 'users/register.html', context)
    
    @staticmethod
    def register2(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'POST':                
                pform = ProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user)
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