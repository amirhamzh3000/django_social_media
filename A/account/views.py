from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post



class UserRegisterView(View):

    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

  
    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})


    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'],email=cd['email'],password=cd['password1'])
            messages.success(request,"you register successfully",'success')
            return redirect('home:home')
        return render(request,self.template_name,{'form':form})
    

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'


    def dispatch(self, request, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)


    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form= self.form_class(request.POST)
        if form.is_valid():
            cd =form.cleaned_data
            user = authenticate(request,username =cd['username'],password = cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you login successfully','success')
                return redirect('home:home')
            messages.warning(request,'username or password is warning','warning')
        return render(request,self.template_name,{'form':form})


class UserLogoutView(LoginRequiredMixin,View):

    def get(self,request):
        logout(request)
        messages.success(request,'you logout successfully','success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin,View):
    
    def get(self,request,user_id):
        user =User.objects.get(id = user_id)
        posts = Post.objects.filter(user =user)
        return render(request,'account/profile.html',{'user': user,'posts':posts})
