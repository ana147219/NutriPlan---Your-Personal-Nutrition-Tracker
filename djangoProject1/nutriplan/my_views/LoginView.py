
"""
Tijana Gasic 0247/2021
Natasa Spasic 0310/2021

"""


from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

class HomeView(TemplateView):
    """
    Class for loading index template
    """
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        """"
        Takes request and loads index page
        """
        return render(request, self.template_name)


class LoginView(TemplateView):
    """
        Class for loading template and user's registration.
    """
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        """
            Takes request and loads the login page.
        """
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """
            From request takes username and
            password and if it finds a user
            with those credentials, it logs
            them in and redirects to the home
            page. Otherwise, it redirects to
            the login page.
        """
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError as e:
            return HttpResponseBadRequest()

        if (username=='' or password==''):
            messages.info(request, "Didnt fill out every field")
            return redirect('login-page')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect('login-page')

class LogoutView(TemplateView):
    """
    Class for logging out user
    """

    def post(self,request,*args, **kwargs):
        """
        Takes request and logs out user and redirects to index page
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        logout(request)

        return redirect('index')