"""
Natasa Spasic 0310/2021
"""


import random

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.models import Group

from nutriplan.my_models.MyUser import MyUser


class SignupView(TemplateView):
    """
        Class that handles users data
        when registration form is submitted.
    """
    template_name = "login.html"

    #username, email, password, gender, userType, verification_code = None, None, None, None, None, None
    dictOfUsers = dict()

    def post(self, request, *args, **kwargs):
        """
            It takes ajax post request and saves data,
            that is later used for creating new user,
            and also generates verification code.
        """
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirmpassword')
            gender = request.POST.get('gender')[0].upper()
            userType = request.POST.get('userType')
        except KeyError as e:
            return HttpResponseBadRequest()

        if MyUser.objects.filter(username=username).exists() or MyUser.objects.filter(email=email).exists():
            return HttpResponseBadRequest('')


        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        SignupView.dictOfUsers[username] = [email, password, confirm_password, gender, userType, verification_code]
        send_mail(
            'Verification Code',
            f'Your verification code is: {verification_code}',
            'nutriplannart@gmail.com',
            [email],
            fail_silently=False,
        )



        return HttpResponse()

class VerifyView(TemplateView):
    """
        Class that saves new user when they register.
    """
    template_name = "login.html"

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
            It takes ajax post request and creates new user if
            verification code is correct. After that takes
            user on login part of page where he can now log in
            with his new account.
        """

        try:
            username = request.POST.get('username')
        except KeyError as e:
            return HttpResponseBadRequest()

        if MyUser.objects.filter(username=username).exists():
            return HttpResponseBadRequest('')

        email, password, confirm_password, gender, userType, verification_code = SignupView.dictOfUsers[username]

        if MyUser.objects.filter(email=email).exists():
            return HttpResponseBadRequest('')
        try:
            code = request.POST['verification_code']
        except KeyError as e:
            return HttpResponseBadRequest()
        if code != verification_code:
            return JsonResponse({'success': False, 'message': 'Invalid verification code. Please try again.'})
        else:
            user = MyUser.objects.create_user(username=username, email=email,
                                              password=password, gender=gender)
            user.save()
            if userType == 'nutri_user':
                group, created = Group.objects.get_or_create(name='Nutricionist')
                user.groups.add(group)

            return JsonResponse({'success': True, 'message': 'Verification successful.'})


class CheckUsernameView(TemplateView):
    """
        Checks if the username entered is available.
    """
    def get(self, request):
        username = request.GET.get('username')
        if MyUser.objects.filter(username=username).exists():
            return JsonResponse({'available': False})
        else:
            return JsonResponse({'available': True})

class CheckEmailView(TemplateView):
    """
        Checks if the email entered is available.
    """
    def get(self, request):
        email = request.GET.get('email')
        if MyUser.objects.filter(email=email).exists():
            return JsonResponse({'available': False})
        else:
            return JsonResponse({'available': True})

class ForgotPasswordView(TemplateView):
    """
        Class that saves data of user that wants
        to change their password.
    """
    dictOfUsers = dict()
    def post(self, request, *args, **kwargs):
        """
            It takes ajax post request and saves data
            of user and generates verification code.
        """
        email = request.POST.get('email')
        password = request.POST.get('password')

        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        # Send verification email
        send_mail(
            'Verification Code',
            f'Your verification code for changing password is: {verification_code}',
            'nutriplannart@gmail.com',
            [email],
            fail_silently=False,
        )
        ForgotPasswordView.dictOfUsers[email] = [password, verification_code]

        return HttpResponse()


class ChangePasswordView(TemplateView):
    """
        Class that changes users password.
    """
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        """
            It takes ajax post request and changes users password
            if verification code is correct. After that takes
            user on login part of page where he can now log in
            with his new password.
        """
        email = request.POST.get('email')
        try:
            code = request.POST['verification_code']
        except KeyError as e:
            return HttpResponseBadRequest()
        password, verification_code = ForgotPasswordView.dictOfUsers[email]
        if code != verification_code:
            return JsonResponse({'success': False, 'message': 'Invalid verification code. Please try again.'})
        else:
            user = MyUser.objects.get(email=email)
            user.set_password(password)
            user.save()
            return JsonResponse({'success': True, 'message': 'Verification successful.'})

class ResendCodeForgotPassView(TemplateView):
    """
        Class whose responsibility is to resend the code
        when changing password.
    """
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        """
            It takes ajax post request and
            sends verification code again.
        """
        email = request.POST.get('email')
        password, verification_code = ForgotPasswordView.dictOfUsers[email]
        send_mail(
            'Verification Code',
            f'Your verification code for changing password is: {verification_code}',
            'nutriplannart@gmail.com',
            [email],
            fail_silently=False,
        )

        return JsonResponse({'message': 'Verification code resent successfully'})


class ResendCodeSignupView(TemplateView):
    """
        Class whose responsibility is to resend the code
        when signing up in app.
    """
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        """
            It takes ajax post request and
            sends verification code again.
        """
        username = request.POST.get('username')
        print(username)
        email, password, confirm_password, gender, userType, verification_code = SignupView.dictOfUsers[username]
        print(email, password, confirm_password, gender, userType, verification_code)
        send_mail(
            'Verification Code',
            f'Your verification code is: {verification_code}',
            'nutriplannart@gmail.com',
            [email],
            fail_silently=False,
        )

        return JsonResponse({'message': 'Verification code resent successfully'})