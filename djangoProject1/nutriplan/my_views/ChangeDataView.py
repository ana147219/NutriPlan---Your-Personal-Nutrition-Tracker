"""
Natasa Spasic 0310/2021
"""

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib import messages

from nutriplan.my_models.MyUser import MyUser


class ChangeDataView(TemplateView):
    """
        Class provides functionality for
        changing data of user (name, password or type of user).
    """
    template_name = "home.html"

    @method_decorator(login_required(login_url='login-page'))
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
            It takes request and depending on
            entered data, it saves the user's
            modified information. After that
            it takes him on home page.
        """
        user = request.user
        print("user: "+user.get_username())
        if MyUser.objects.filter(username=request.POST['username']).exists():
            messages.info(request, 'open_popup')
            messages.error(request, 'This username is taken')
            return redirect('home')
        if (request.POST['password'] != request.POST['confirm-password']):
            messages.info(request, 'open_popup')
            messages.error(request, 'Passwords don`t match')
            return redirect('home')

        #print(request.POST['password'])
        #print(request.POST['confirm-password'])
        #print(request.POST['username'])
        #print(request.POST['nutricionist'])
        if  request.POST['password']!="":
            user.set_password( request.POST['password'])
        if request.POST['username'] != "" :
            user.username = request.POST['username']
        user.save()

        if request.POST.get('nutricionist') == 'Nutricionist':
            group, created = Group.objects.get_or_create(name='Nutricionist')
            user.groups.add(group)
        else:
            nutricionist_group = Group.objects.get(name='Nutricionist')
            if user.groups.filter(name='Nutricionist').exists():
                user.groups.remove(nutricionist_group)

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        return redirect('home')
